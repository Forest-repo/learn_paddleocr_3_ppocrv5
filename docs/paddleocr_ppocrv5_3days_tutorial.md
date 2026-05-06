# PaddleOCR PP-OCRv5 3 天实战教程

本文目标：3 天内完成 PaddleOCR PP-OCRv5 的本地部署、推理、结果格式理解、数据标注、检测/识别训练、模型导出和自训练模型接入。

官方入口：

- PaddleOCR GitHub: https://github.com/PaddlePaddle/PaddleOCR
- PaddleOCR 3.x 文档: https://paddlepaddle.github.io/PaddleOCR/main/en/
- OCR 管线使用: https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/pipeline_usage/OCR.html

## 你要先建立的认知

OCR 不是一个单独模型，常见完整流程是：

```text
原图
  -> 文档方向分类，可选
  -> 文档矫正，可选
  -> 文本检测，找文字框
  -> 文本行方向分类，可选
  -> 文本识别，识别框内文字
  -> 输出坐标、文字、置信度
```

训练时也要分开看：

- 检测模型：负责“文字在哪里”。
- 识别模型：负责“框里的文字是什么”。
- 方向分类器：负责“文字是否旋转了”，大多数入门场景可以先不训练。

最快路线：

1. 第 1 天跑通官方 PP-OCRv5 推理。
2. 第 2 天学会标注和数据格式。
3. 第 3 天分别跑通检测/识别微调命令，并导出模型。

## 第 1 天目标

产出：

- 本地环境能 import `paddleocr`。
- 单张图片能输出 OCR JSON。
- 批量图片能保存 JSON。
- 能把 OCR 行结果另存成 CSV。
- 能看懂结果里的文字、坐标和置信度。

重点文件：

- [day1_install_and_infer.md](day1_install_and_infer.md)
- [../examples/infer_single_image.py](../examples/infer_single_image.py)
- [../examples/infer_batch_images.py](../examples/infer_batch_images.py)
- [../examples/save_ocr_result_json.py](../examples/save_ocr_result_json.py)
- [../examples/save_ocr_result_csv.py](../examples/save_ocr_result_csv.py)

## 第 2 天目标

产出：

- 知道检测和识别训练数据格式不同。
- 会用 PPOCRLabel 标注图片。
- 能整理出检测训练集。
- 能整理出识别训练集。
- 知道字典文件为什么会影响识别训练。

重点文件：

- [day2_annotation_and_dataset.md](day2_annotation_and_dataset.md)
- [../datasets/README.md](../datasets/README.md)
- [../datasets/det_dataset_template/train.txt](../datasets/det_dataset_template/train.txt)
- [../datasets/rec_dataset_template/train.txt](../datasets/rec_dataset_template/train.txt)

## 第 3 天目标

产出：

- 能看懂检测训练命令。
- 能看懂识别训练命令。
- 能知道配置文件该改哪些字段。
- 能导出 inference 模型。
- 能用自训练模型重新推理。

重点文件：

- [day3_train_export_infer.md](day3_train_export_infer.md)
- [../configs_notes/det_train_config_notes.md](../configs_notes/det_train_config_notes.md)
- [../configs_notes/rec_train_config_notes.md](../configs_notes/rec_train_config_notes.md)
- [../examples/infer_with_custom_model.py](../examples/infer_with_custom_model.py)

## 3 天安排表

### Day 1 上午：安装

1. 新建虚拟环境。
2. 安装 PaddlePaddle。
3. 安装 PaddleOCR。
4. 确认 `paddle` 和 `paddleocr` 能 import。

CPU 优先，因为快且稳定。GPU 可以作为第二阶段优化。

### Day 1 下午：推理和结果格式

1. 单张图片推理。
2. 输出 JSON。
3. 批量图片推理。
4. 保存 CSV。
5. 对照图片看坐标和置信度。

### Day 2 上午：理解训练对象

先问自己两个问题：

- 默认模型有没有框中文字？
- 框出来以后识别内容对不对？

如果框都没框对，优先训练检测。如果框正确但文字错，优先训练识别。

### Day 2 下午：标注和数据整理

1. 用 PPOCRLabel 标注整图。
2. 导出检测标签。
3. 裁剪文本行，整理识别标签。
4. 检查字典。
5. 小规模抽样检查 20 张图。

### Day 3 上午：训练检测/识别

1. 克隆官方 PaddleOCR 仓库。
2. 复制官方 PP-OCRv5 配置。
3. 修改数据路径和输出路径。
4. 小批量跑通训练。
5. 做一次评估。

### Day 3 下午：导出和接入

1. 导出检测 inference 模型。
2. 导出识别 inference 模型。
3. 用 `infer_with_custom_model.py` 加载模型推理。
4. 保存输出结果。
5. 记录失败样本，进入下一轮数据补充。

## 最容易踩坑的地方

- 把检测数据格式和识别数据格式混在一起。
- 识别标签里的字符不在字典里。
- 训练时路径写错，Windows 反斜杠转义出问题。
- 直接从零训练，数据量不够导致效果很差。
- 只看 loss，不看真实图片上的推理结果。
- 默认模型其实已经够用，却过早训练检测模型。
- 训练好了模型，但推理时忘了指定自定义字典。

