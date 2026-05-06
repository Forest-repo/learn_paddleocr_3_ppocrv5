# 第 1 天：安装 PP-OCRv5 并推理图片

目标：最快速度让 PaddleOCR PP-OCRv5 在本地跑起来，并看懂返回结果。

## 1. 环境建议

Windows 推荐：

```text
Python: 3.9 - 3.12 之间优先选官方支持范围内的稳定版本
系统: Windows 10/11
显卡: 没有 GPU 也可以先用 CPU
```

为了最快跑通，先选 CPU。CPU 慢一点，但环境坑少。

## 2. CPU 安装

在项目根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install paddlepaddle
pip install paddleocr
```

也可以参考仓库里的脚本：

```powershell
.\scripts\install_cpu.ps1
```

## 3. GPU 安装

GPU 先确认：

```powershell
nvidia-smi
```

然后去 PaddlePaddle 官方安装选择器选择与你驱动、CUDA、Python 匹配的命令：

```text
https://www.paddlepaddle.org.cn/install/quick
```

通用思路：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install paddlepaddle-gpu
pip install paddleocr
```

注意：GPU 不是越早越好。先 CPU 跑通推理和数据格式，再处理 CUDA 版本问题会更省时间。

## 4. 验证安装

```powershell
python -c "import paddle; import paddleocr; print(paddle.__version__); print(paddleocr.__version__)"
```

如果要看 GPU 是否可用：

```powershell
python -c "import paddle; print(paddle.device.is_compiled_with_cuda())"
```

## 5. 单张图片推理

准备一张图片，比如：

```text
images/test.jpg
```

最快确认官方命令行是否能工作：

```powershell
paddleocr ocr -i images\test.jpg `
  --use_doc_orientation_classify False `
  --use_doc_unwarping False `
  --use_textline_orientation False `
  --save_path output `
  --device cpu
```

如果模型下载默认源访问慢，可以先在当前 PowerShell 会话里设置：

```powershell
$env:PADDLE_PDX_MODEL_SOURCE="BOS"
```

然后再跑推理命令。

执行：

```powershell
python examples\infer_single_image.py --image images\test.jpg --device cpu
```

保存 JSON：

```powershell
python examples\infer_single_image.py --image images\test.jpg --device cpu --json-out outputs\test.json
```

如果要强制使用 server 模型：

```powershell
python examples\infer_single_image.py --image images\test.jpg --device cpu --model-size server --json-out outputs\test_server.json
```

如果图片中有旋转文本：

```powershell
python examples\infer_single_image.py --image images\test.jpg --use-textline-orientation --json-out outputs\test_orientation.json
```

## 6. 批量图片推理

```powershell
python examples\infer_batch_images.py --input-dir images --output-dir outputs\json --device cpu
```

输出：

```text
outputs/json/
  xxx.json
  yyy.json
  _summary.json
```

## 7. 保存为 JSON

```powershell
python examples\save_ocr_result_json.py --image images\test.jpg --output outputs\ocr_result.json
```

JSON 是最完整的格式，建议优先保存。后续训练数据清洗、人工复核、前端展示都更方便。

## 8. 保存为 CSV

```powershell
python examples\save_ocr_result_csv.py --image images\test.jpg --output outputs\ocr_result.csv
```

CSV 适合给业务同学看，核心字段：

```text
page_index,line_index,text,score,box
```

## 9. 结果格式怎么看

PaddleOCR 3.x 的结果通常会包含这些高价值字段：

```text
rec_texts    识别出的文本列表
rec_scores   每一行文本的识别置信度
dt_polys     检测框四点坐标
rec_boxes    识别框矩形坐标，具体取决于版本和配置
```

你可以这样理解：

```json
{
  "rec_texts": ["姓名", "张三"],
  "rec_scores": [0.99, 0.98],
  "dt_polys": [
    [[10, 20], [80, 20], [80, 50], [10, 50]],
    [[100, 20], [180, 20], [180, 50], [100, 50]]
  ]
}
```

每个 `dt_polys` 是一个文本框，通常是顺时针或接近顺时针的四个点。

## 10. 第一天验收标准

你完成这些就算第 1 天成功：

- 能 import `paddleocr`。
- 能对一张图片输出 JSON。
- 能批量处理一个图片目录。
- 能把结果保存成 CSV。
- 能解释每一行文本对应的坐标和置信度。
