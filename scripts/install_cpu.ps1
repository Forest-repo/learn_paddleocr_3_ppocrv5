# Windows CPU quick install for PaddleOCR PP-OCRv5.
# Run manually in PowerShell after reviewing the tutorial.

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel

# PaddleOCR 3.x package. The default OCR pipeline uses PP-OCRv5 models.
pip install paddleocr

# CPU PaddlePaddle. If this fails, check the official PaddlePaddle install page
# for the exact wheel matching your Python version and OS.
pip install paddlepaddle

@'
import paddle
import paddleocr
print("paddle:", paddle.__version__)
print("paddleocr:", paddleocr.__version__)
'@ | python
