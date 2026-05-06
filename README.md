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

## 官方资料

- PaddleOCR GitHub: https://github.com/PaddlePaddle/PaddleOCR
- PaddleOCR 3.x 文档: https://paddlepaddle.github.io/PaddleOCR/main/en/
- OCR 管线使用文档: https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/pipeline_usage/OCR.html
- PP-OCRv5 训练说明: https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/module_usage/text_detection.html
