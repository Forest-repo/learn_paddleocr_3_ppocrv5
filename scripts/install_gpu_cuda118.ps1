# Windows GPU quick install for PaddleOCR PP-OCRv5.
# Run manually only if your NVIDIA driver/CUDA stack matches the wheel.

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip setuptools wheel

# Pick the PaddlePaddle GPU wheel from the official install selector:
# https://www.paddlepaddle.org.cn/install/quick
# The line below is only a common CUDA 11.8 example; adjust if needed.
pip install paddlepaddle-gpu

pip install paddleocr

@'
import paddle
import paddleocr
print("paddle:", paddle.__version__)
print("paddleocr:", paddleocr.__version__)
print("compiled with cuda:", paddle.device.is_compiled_with_cuda())
'@ | python
