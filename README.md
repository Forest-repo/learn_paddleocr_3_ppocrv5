# PaddleOCR PP-OCRv5 3 天游教程

这个仓库用于快速跑通 PaddleOCR PP-OCRv5 的本地部署、图片推理、结果格式理解、数据标注、检测/识别模型训练、导出和自训练模型接入。

> 目标不是一开始就做生产级 OCR 系统，而是在 3 天内建立完整闭环：能跑、能看懂结果、知道怎么准备数据、知道训练检测和识别分别怎么做。

## 推荐阅读顺序

1. [3 天总教程](docs/paddleocr_ppocrv5_3days_tutorial.md)
2. [第 1 天：安装与推理](docs/day1_install_and_infer.md)
3. [第 2 天：标注与数据集](docs/day2_annotation_and_dataset.md)
4. [第 3 天：训练、导出、自训练模型推理](docs/day3_train_export_infer.md)
5. [常见坑排查](docs/troubleshooting.md)

## 示例脚本

```text
examples/
  infer_single_image.py          # 单张图片推理
  infer_batch_images.py          # 批量图片推理
  save_ocr_result_json.py        # 推理结果保存 JSON
  save_ocr_result_csv.py         # 推理结果保存 CSV
  infer_with_custom_model.py     # 加载自训练模型推理

tools/
  check_rec_label_dict.py        # 检查识别标签字符是否被字典覆盖
```

## 数据集模板

```text
datasets/
  det_dataset_template/          # 文本检测训练数据模板
  rec_dataset_template/          # 文本识别训练数据模板
```

## OCR 核心原理：检测、识别和 CTC

一个完整 OCR 流程通常不是直接把整张图丢进去就输出文字，而是拆成两个核心阶段：

```text
图片
  -> 文本检测模型：找哪里有文字
  -> 文本识别模型：判断框里的文字是什么
  -> 结构化结果：内容、置信度、坐标
```

在 PaddleOCR 的输出 JSON 里，可以这样理解：

```text
dt_polys / rec_polys / rec_boxes  文本框坐标
rec_texts                         识别出来的文字内容
rec_scores                        文本识别置信度
```

`rec_scores` 是识别模型的置信度，不是检测模型的置信度。它回答的是：“识别模型有多确定这个框里的文字就是这个结果？”例如：

```text
COMMERCIAL INVOICE: 0.9871
中: 0.2620
```

第一个结果可信度很高，第二个结果可信度很低，后续人工复核或业务规则可以优先关注低分结果。

### 1. 文本检测模型做什么

文本检测模型负责在图片里找文本位置。它输出的是框，也就是坐标：

```text
[
  [左上x, 左上y],
  [右上x, 右上y],
  [右下x, 右下y],
  [左下x, 左下y]
]
```

这类四点框可以表达倾斜文本，比简单矩形更灵活。检测阶段通常只关心“哪里像文字”，不负责判断具体内容是 `A`、`B` 还是中文。

### 2. 文本识别模型做什么

文本识别模型拿到检测框后，会把框里的文字区域裁剪出来，再识别成字符串：

```text
一张文字行图片 -> 识别模型 -> 一串字符
```

它不是简单地先把每个字符切开，再逐个分类。早期 OCR 常这么做，但现代 OCR 通常避免手工切字，因为字符切割很难：

- 字母可能连在一起。
- 字体、字号、间距变化很大。
- 图片可能倾斜、模糊、有噪声。
- 中文没有天然空格，字符边界不总是清楚。

所以现代识别模型更常见的做法是：把整行文本图片当成一个序列来识别。

### 3. CTC 识别方式是什么

CTC 全称是 `Connectionist Temporal Classification`。它的核心作用是：在不知道每个字符具体对应图片哪个位置的情况下，也能训练序列识别模型。

可以把一行文字图片想象成一条从左到右的序列：

```text
图片宽度方向：左 ---------------------------------> 右
```

模型沿着宽度方向提取特征，在很多个位置上分别预测字符概率。比如目标文字是：

```text
COM
```

模型内部可能输出很多个时间步：

```text
t1: C
t2: C
t3: blank
t4: O
t5: O
t6: blank
t7: M
t8: M
```

这里的 `blank` 是 CTC 额外加入的空白类别，表示“这个位置不输出字符”。

CTC 解码规则很简单：

```text
先合并连续重复字符，再去掉 blank
```

所以上面的输出会变成：

```text
C C blank O O blank M M
-> C blank O blank M
-> COM
```

这就是为什么模型不需要提前把图片切成 `C`、`O`、`M` 三个小图，也能得到最终文本。

### 4. CTC 模型是不是 CNN

CTC 本身不是 CNN，它是一种序列训练和解码方法。识别模型的网络结构可以有很多种，常见形式是：

```text
文字行图片
  -> CNN / 视觉骨干网络提取图像特征
  -> 序列建模层
  -> 每个时间步输出字符概率
  -> CTC 解码
  -> 最终文本
```

早期常见结构叫 `CRNN`：

```text
CNN + RNN + CTC
```

现在也可能是：

```text
CNN + Transformer + CTC
CNN + SVTR-like 模块 + CTC
```

网络结构可以变化，但 CTC 的核心思想不变：让模型从整行图片中输出字符序列，而不是依赖手工切字符。

### 5. CTC Loss 是什么

训练识别模型时，数据通常只有整行文本标签：

```text
图片 -> "COMMERCIAL"
```

但没有标注每个字符在图片中的精确位置：

```text
C 在第 1-10 像素
O 在第 11-20 像素
M 在第 21-30 像素
```

CTC Loss 正是为了解决这个问题。它会把所有能够解码成正确文本的路径概率加起来。

比如目标是：

```text
COM
```

下面这些路径都可以通过 CTC 解码得到 `COM`：

```text
C C blank O O blank M
C blank O O M M blank
blank C C O blank M M
```

CTC 会计算：

```text
P("COM" | 图片) = 所有能解码成 "COM" 的路径概率之和
```

训练损失就是：

```text
CTC Loss = -log P("COM" | 图片)
```

训练目标是让正确文本的总概率越来越高，也就是让 loss 越来越低。

### 6. 一句话总结

OCR 可以先这样建立直觉：

```text
检测模型：负责找位置，输出坐标。
识别模型：负责读内容，输出文字和识别置信度。
CTC：让模型不用切字符，也能从整行图片学到字符序列。
CTC Loss：在没有字符级位置标注的情况下，训练模型输出正确文本。
```

## 官方资料

- PaddleOCR GitHub: https://github.com/PaddlePaddle/PaddleOCR
- PaddleOCR 3.x 文档: https://paddlepaddle.github.io/PaddleOCR/main/en/
- OCR 管线使用文档: https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/pipeline_usage/OCR.html
- PP-OCRv5 训练说明: https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/module_usage/text_detection.html
