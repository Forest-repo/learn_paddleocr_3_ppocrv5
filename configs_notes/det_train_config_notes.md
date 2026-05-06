# 文本检测训练配置改动说明

你训练检测模型时，核心是从官方配置复制一份到自己的项目里，然后只改必要字段。

## 推荐起点

优先从 PaddleOCR 官方仓库里找 PP-OCRv5 检测配置，例如：

```text
configs/det/PP-OCRv5/PP-OCRv5_server_det.yml
configs/det/PP-OCRv5/PP-OCRv5_mobile_det.yml
```

如果你的仓库版本中文件名略有变化，用下面命令搜索：

```powershell
Get-ChildItem PaddleOCR\configs\det -Recurse -Filter "*OCRv5*yml"
```

## 必改字段

```yaml
Global:
  pretrained_model: ./PP-OCRv5_server_det_pretrained.pdparams
  save_model_dir: output/det_ppocrv5
  eval_batch_step: [0, 1000]
  epoch_num: 100

Train:
  dataset:
    data_dir: ./datasets/det_dataset
    label_file_list:
      - ./datasets/det_dataset/train.txt

Eval:
  dataset:
    data_dir: ./datasets/det_dataset
    label_file_list:
      - ./datasets/det_dataset/val.txt
```

## 小样本建议

- 先用 20-100 张图跑通训练流程。
- batch size 从 2 或 4 开始，显存充足再加。
- 图像分辨率太大容易爆显存，先按官方默认。
- 如果是特定票据、表单、屏幕截图，检测模型微调通常比从零训练更稳。

## 判断是否需要训练检测

需要训练检测的典型情况：

- 默认模型漏检你的业务字体、印章、低清图、竖排文字。
- 文本框经常框不全或把多行框成一块。
- 场景很特殊，比如工业喷码、仪表盘、票据边缘小字。

暂时不需要训练检测的情况：

- 默认模型能稳定框出文字，只是识别错字。
- 你的主要问题是专业词、型号、特殊符号识别不准。
