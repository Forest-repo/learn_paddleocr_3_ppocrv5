# PaddleOCR 数据集模板说明

OCR 训练通常分成两个任务：

- 文本检测：输入整张图，学习“文字在哪里”。
- 文本识别：输入裁剪后的单行/单词图片，学习“这段图里的文字是什么”。

所以你经常需要准备两套格式：

```text
datasets/
  det_dataset_template/
    images/
    train.txt
    val.txt
  rec_dataset_template/
    images/
    train.txt
    val.txt
    dict.txt
```

## 检测数据

检测数据一般是一张原图对应多行文本框标注。每行格式通常是：

```text
图片路径\t[{"transcription":"文字","points":[[x1,y1],[x2,y2],[x3,y3],[x4,y4]]}]
```

## 识别数据

识别数据一般是“裁剪好的文本行图片 + 文本标签”。每行格式通常是：

```text
图片路径\t文本内容
```

## 推荐流程

1. 用 PPOCRLabel 标注整图。
2. 导出检测训练标签。
3. 从检测框裁剪文本行，生成识别训练图片。
4. 检查识别标签中的所有字符是否都在字典文件里。
5. 先小规模训练 20-100 张图，确认格式无误，再扩大训练。

