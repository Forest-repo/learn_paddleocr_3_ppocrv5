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

在项目根目录执行： conda create --name paddle32_ppocrv5 python=3.11

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

## 10. OCR 结果 JSON 详细说明

PaddleOCR 保存到 `output` 目录下的 `*_res.json`，整体可以分成三类：输入信息、模型配置、OCR 结果。

最关键的是这几组字段：

```json
"rec_texts": [...]
"rec_scores": [...]
"rec_polys": [...]
"rec_boxes": [...]
```

它们是按下标一一对应的。比如：

```text
rec_texts[0]  -> "COMMERCIAL INVOICE"
rec_scores[0] -> 0.9870749711990356
rec_polys[0]  -> [[458, 73], [740, 73], [740, 104], [458, 104]]
rec_boxes[0]  -> [458, 73, 740, 104]
```

意思是：第 1 个识别结果内容是 `COMMERCIAL INVOICE`，置信度约 `0.9871`，它在图片上的位置是这个四边形区域。

字段解释：

```text
input_path       输入图片路径。
page_index       页码索引。单张图片一般是 null；如果是 PDF 或多页输入，可能会有页码。
model_settings   这次 OCR 开启/关闭了哪些模型能力。
dt_polys         detection 阶段找到的文本框，每个元素是一个四点坐标框。顺时针方向，四个点
rec_texts        识别出来的文本内容列表。
rec_scores       每条文本的识别置信度，越接近 1 越可信。
rec_polys        识别结果对应的四点坐标，一般和 dt_polys 很接近。顺时针方向，四个点  
rec_boxes        矩形框坐标，格式是 [x_min, y_min, x_max, y_max]。
```

`model_settings` 示例：

```json
{
  "use_doc_preprocessor": false,
  "use_textline_orientation": false
}
```

这里表示没有启用文档预处理，也没有启用文本行方向分类。

`dt_polys` 和 `rec_polys` 的四点坐标格式通常是：

```text
[
  [左上x, 左上y],
  [右上x, 右上y],
  [右下x, 右下y],
  [左下x, 左下y]
]
```

`rec_boxes` 比 `rec_polys` 简单，但只能表达水平矩形框，不能表达倾斜框。

`rec_polys` 不是识别模型重新预测出来的新坐标。更准确地说：

```text
dt_polys   检测阶段输出的文本框。
rec_polys  最终识别结果对应的文本框。
```

OCR pipeline 中间通常是这样的：

```text
检测模型输出 dt_polys
  -> 按框裁剪图片
  -> 可选：方向分类、旋转校正
  -> 文本识别
  -> 可选：按 text_rec_score_thresh 过滤低置信度结果
  -> 输出 rec_texts / rec_scores / rec_polys
```

所以 `dt_polys` 更偏“检测阶段原始找到的框”，`rec_polys` 更偏“最终识别结果对应的框”。如果中间有过滤、排序或其他后处理，检测出来的框不一定都会进入最终识别结果。

在当前示例里，因为流程比较简单，而且没有过滤掉结果，所以 `dt_polys` 和 `rec_polys` 基本一样。但做 `(内容, 置信度, 坐标)` 三元组时，用 `rec_polys` 更合适，因为它和最终的 `rec_texts`、`rec_scores` 天然一一对应。

如果要在代码里保存“内容、置信度、坐标”，可以把这三个数组按下标组合起来：

```python
ocr_items = list(zip(rec_texts, rec_scores, rec_polys))
```

也就是：

```text
(content, confidence, coordinate)
```

对应：

```text
(rec_texts[i], rec_scores[i], rec_polys[i])
```

例如 `费用组-单票-商业发票-007_res.json` 里一共有 30 条识别结果，因为 `rec_texts`、`rec_scores`、`rec_polys`、`rec_boxes` 都是 30 个元素。

## 11. 第一天验收标准

你完成这些就算第 1 天成功：

- 能 import `paddleocr`。
- 能对一张图片输出 JSON。
- 能批量处理一个图片目录。
- 能把结果保存成 CSV。
- 能解释每一行文本对应的坐标和置信度。
