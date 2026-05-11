from paddleocr import PaddleOCR
import time
from pathlib import Path

# 本项目内置的 server 级模型（从官方缓存复制而来，无需联网下载）
# models/PP-OCRv5_server_det/  -- 检测模型（~84 MB）
# models/PP-OCRv5_server_rec/  -- 识别模型（~80 MB）
MODELS_DIR = Path(__file__).parent / "models"
DET_MODEL_DIR = str(MODELS_DIR / "PP-OCRv5_server_det")
REC_MODEL_DIR = str(MODELS_DIR / "PP-OCRv5_server_rec")
TEXTLINE_MODEL_DIR = str(MODELS_DIR / "PP-LCNet_x1_0_textline_ori") # 文本行方向分类模型（~20 MB）
print(f"检测模型目录: {DET_MODEL_DIR}")
print(f"识别模型目录: {REC_MODEL_DIR}")
print(f"文本行方向分类模型目录: {TEXTLINE_MODEL_DIR}")

total_start = time.perf_counter()
init_start = time.perf_counter()
ocr = PaddleOCR(
    text_detection_model_dir=DET_MODEL_DIR,   # 使用本项目的检测模型
    text_recognition_model_dir=REC_MODEL_DIR, # 使用本项目的识别模型
    use_doc_orientation_classify=False, # 通过 use_doc_orientation_classify 参数指定不使用文档方向分类模型
    use_doc_unwarping=False,            # 通过 use_doc_unwarping 参数指定不使用文本图像矫正模型
    use_textline_orientation=True,     # 通过 use_textline_orientation 参数指定不使用文本行方向分类模型
    textline_orientation_model_dir=TEXTLINE_MODEL_DIR, # 指定文本行方向分类模型目录
)
print(f"模型初始化耗时: {time.perf_counter() - init_start:.3f}s")
predict_start = time.perf_counter()
# ocr = PaddleOCR(lang="en") # 通过 lang 参数来使用英文模型
# ocr = PaddleOCR(ocr_version="PP-OCRv4") # 通过 ocr_version 参数来使用 PP-OCR 其他版本
# ocr = PaddleOCR(device="gpu") # 通过 device 参数使得在模型推理时使用 GPU
# ocr = PaddleOCR(
#     text_detection_model_name="PP-OCRv5_server_det",
#     text_recognition_model_name="PP-OCRv5_server_rec",
#     use_doc_orientation_classify=False,
#     use_doc_unwarping=False,
#     use_textline_orientation=False,
# ) # 更换 PP-OCRv5_server 模型

result = ocr.predict("费用组-单票-商业发票-007.png")
print(f"OCR 推理耗时: {time.perf_counter() - predict_start:.3f}s")
save_start = time.perf_counter()
ocr_items = []
for res in result: #result长度为1，res为字典
    rec_texts = res.get("rec_texts", [])
    rec_scores = res.get("rec_scores", [])
    rec_polys = res.get("rec_polys", [])
    ocr_items.extend(zip(rec_texts, rec_scores, rec_polys))
    res.save_to_img("output")
    res.save_to_json("output")
print(f"结果处理耗时: {time.perf_counter() - save_start:.3f}s")
for content, confidence, _coordinate in ocr_items:
    print(f"{content}: {confidence:.4f}")
print(f"总耗时: {time.perf_counter() - total_start:.3f}s")
print("test")


