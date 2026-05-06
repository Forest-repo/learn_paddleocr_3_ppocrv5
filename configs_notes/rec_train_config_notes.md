# 文本识别训练配置改动说明

识别模型训练的核心是：图片必须是裁剪好的文本行，标签必须和字典匹配。

## 推荐起点

从 PaddleOCR 官方仓库复制 PP-OCRv5 识别配置，例如：

```text
configs/rec/PP-OCRv5/PP-OCRv5_server_rec.yml
configs/rec/PP-OCRv5/PP-OCRv5_mobile_rec.yml
```

如果文件名有变化，用下面命令搜索：

```powershell
Get-ChildItem PaddleOCR\configs\rec -Recurse -Filter "*OCRv5*yml"
```

## 必改字段

```yaml
Global:
  pretrained_model: ./PP-OCRv5_server_rec_pretrained.pdparams
  save_model_dir: output/rec_ppocrv5
  character_dict_path: ./datasets/rec_dataset/dict.txt
  max_text_length: 25
  use_space_char: true

Train:
  dataset:
    data_dir: ./datasets/rec_dataset
    label_file_list:
      - ./datasets/rec_dataset/train.txt

Eval:
  dataset:
    data_dir: ./datasets/rec_dataset
    label_file_list:
      - ./datasets/rec_dataset/val.txt
```

## 字典文件注意事项

- 标签里出现的每个字符都必须在字典里。
- 中文、英文、数字、符号要逐个检查。
- 如果要识别空格，开启 `use_space_char: true`。
- 字典变了，导出和推理时也必须使用同一份字典。

## 判断是否需要训练识别

需要训练识别的典型情况：

- 检测框位置正确，但文字识别错。
- 业务里有大量型号、批号、专业词、冷门字符。
- 图片来自固定设备，字体或成像风格和通用数据差异大。

暂时不需要训练识别的情况：

- 默认模型已经能识别主要文本。
- 问题主要是漏检或框偏，这时先看检测模型。
