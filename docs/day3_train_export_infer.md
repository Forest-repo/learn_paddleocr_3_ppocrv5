# 第 3 天：训练、导出和自训练模型推理

目标：跑通检测/识别模型微调、评估、导出，并加载自训练模型推理。

## 1. 训练前准备

训练建议直接使用官方 PaddleOCR 仓库。

```powershell
git clone https://github.com/PaddlePaddle/PaddleOCR.git
cd PaddleOCR
pip install -r requirements.txt
```

如果你只安装了 `paddleocr` 包，它适合推理；训练通常需要完整仓库代码、配置文件和训练脚本。

## 2. 找 PP-OCRv5 配置

在官方仓库里搜索配置：

```powershell
Get-ChildItem configs -Recurse -Filter "*OCRv5*yml"
```

重点看：

```text
configs/det/PP-OCRv5/
configs/rec/PP-OCRv5/
```

如果官方仓库版本更新导致文件名变化，以实际搜索结果为准。

## 3. 训练检测模型

下载官方 PP-OCRv5 检测预训练模型：

```powershell
Invoke-WebRequest `
  -Uri https://paddle-model-ecology.bj.bcebos.com/paddlex/official_pretrained_model/PP-OCRv5_server_det_pretrained.pdparams `
  -OutFile PP-OCRv5_server_det_pretrained.pdparams
```

先复制官方检测配置：

```powershell
Copy-Item configs\det\PP-OCRv5\PP-OCRv5_server_det.yml configs\det\PP-OCRv5\my_det.yml
```

然后改：

```yaml
Global:
  pretrained_model: ./PP-OCRv5_server_det_pretrained.pdparams
  save_model_dir: output/det_ppocrv5

Train:
  dataset:
    data_dir: E:/Git_repo/learn_paddleocr_3_ppocrv5/datasets/det_dataset
    label_file_list:
      - E:/Git_repo/learn_paddleocr_3_ppocrv5/datasets/det_dataset/train.txt

Eval:
  dataset:
    data_dir: E:/Git_repo/learn_paddleocr_3_ppocrv5/datasets/det_dataset
    label_file_list:
      - E:/Git_repo/learn_paddleocr_3_ppocrv5/datasets/det_dataset/val.txt
```

Windows 建议在 YAML 里用 `/`，少用 `\`，因为反斜杠容易和转义混在一起。

训练命令：

```powershell
python tools\train.py -c configs\det\PP-OCRv5\my_det.yml `
  -o Global.pretrained_model=./PP-OCRv5_server_det_pretrained.pdparams
```

评估命令：

```powershell
python tools\eval.py -c configs\det\PP-OCRv5\my_det.yml `
  -o Global.pretrained_model=output/det_ppocrv5/best_accuracy.pdparams
```

断点续训：

```powershell
python tools\train.py -c configs\det\PP-OCRv5\my_det.yml -o Global.checkpoints=output/det_ppocrv5/latest
```

导出检测模型：

```powershell
python tools\export_model.py -c configs\det\PP-OCRv5\my_det.yml `
  -o Global.pretrained_model=output/det_ppocrv5/best_accuracy.pdparams `
  Global.save_inference_dir=output/det_export
```

## 4. 训练识别模型

下载官方 PP-OCRv5 识别预训练模型：

```powershell
Invoke-WebRequest `
  -Uri https://paddle-model-ecology.bj.bcebos.com/paddlex/official_pretrained_model/PP-OCRv5_server_rec_pretrained.pdparams `
  -OutFile PP-OCRv5_server_rec_pretrained.pdparams
```

先复制官方识别配置：

```powershell
Copy-Item configs\rec\PP-OCRv5\PP-OCRv5_server_rec.yml configs\rec\PP-OCRv5\my_rec.yml
```

然后改：

```yaml
Global:
  pretrained_model: ./PP-OCRv5_server_rec_pretrained.pdparams
  save_model_dir: output/rec_ppocrv5
  character_dict_path: E:/Git_repo/learn_paddleocr_3_ppocrv5/datasets/rec_dataset/dict.txt
  use_space_char: true

Train:
  dataset:
    data_dir: E:/Git_repo/learn_paddleocr_3_ppocrv5/datasets/rec_dataset
    label_file_list:
      - E:/Git_repo/learn_paddleocr_3_ppocrv5/datasets/rec_dataset/train.txt

Eval:
  dataset:
    data_dir: E:/Git_repo/learn_paddleocr_3_ppocrv5/datasets/rec_dataset
    label_file_list:
      - E:/Git_repo/learn_paddleocr_3_ppocrv5/datasets/rec_dataset/val.txt
```

训练命令：

```powershell
python tools\train.py -c configs\rec\PP-OCRv5\my_rec.yml `
  -o Global.pretrained_model=./PP-OCRv5_server_rec_pretrained.pdparams
```

评估命令：

```powershell
python tools\eval.py -c configs\rec\PP-OCRv5\my_rec.yml `
  -o Global.pretrained_model=output/rec_ppocrv5/best_accuracy.pdparams
```

断点续训：

```powershell
python tools\train.py -c configs\rec\PP-OCRv5\my_rec.yml -o Global.checkpoints=output/rec_ppocrv5/latest
```

导出识别模型：

```powershell
python tools\export_model.py -c configs\rec\PP-OCRv5\my_rec.yml `
  -o Global.pretrained_model=output/rec_ppocrv5/best_accuracy.pdparams `
  Global.save_inference_dir=output/rec_export
```

## 5. 加载自训练模型推理

回到本教程仓库：

```powershell
python examples\infer_with_custom_model.py `
  --image images\test.jpg `
  --det-model-dir PaddleOCR\output\det_export `
  --rec-model-dir PaddleOCR\output\rec_export `
  --output outputs\custom_model_result.json
```

PaddleOCR 3.x 新 API 主要使用：

```text
text_detection_model_dir
text_recognition_model_dir
```

导出的模型目录通常包含：

```text
inference.json
inference.pdiparams
inference.yml
```

识别模型的后处理和字典配置要和训练保持一致。3.x 通常通过导出目录里的 `inference.yml` 记录这些信息；如果你用的是旧版 2.x 命令行，才经常会看到 `rec_char_dict_path` 这种参数。

如果只训练了识别模型，可以先继续使用官方检测模型，只指定识别模型。当前示例脚本为了流程清晰，默认要求同时传检测和识别模型；你可以根据需要删掉检测模型参数，保留官方默认检测。

## 6. 什么时候训练检测，什么时候训练识别

优先训练检测：

- 默认模型漏框。
- 框位置偏。
- 多行粘在一起。
- 小字、倾斜文字、特殊背景检测不好。

优先训练识别：

- 框准确，但字错。
- 业务术语、编号、型号识别不好。
- 特殊字符、繁体字、生僻字多。

两个都训练：

- 场景和通用 OCR 差异很大。
- 默认模型既漏检又识别错。
- 你要做较高精度的业务系统。

## 7. 三天内的现实训练策略

不要从零训练。三天内最稳的是微调：

1. 先用官方模型推理 100 张业务图。
2. 找出失败样本。
3. 标注 50-200 张高价值样本。
4. 先微调识别模型。
5. 如果框不准，再微调检测模型。
6. 导出模型，回到真实图片测试。

## 8. 第三天验收标准

你完成这些就算第 3 天成功：

- 知道训练脚本在哪里。
- 知道配置文件要改哪些字段。
- 能区分检测训练和识别训练。
- 能导出 inference 模型。
- 能用自训练模型重新推理。
- 知道下一轮该补哪些数据。
