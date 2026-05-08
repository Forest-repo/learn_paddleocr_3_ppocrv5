# 验证安装是否成功
import paddleocr
print(f"PaddleOCR版本: {paddleocr.__version__}")

# 若使用本地推理引擎 paddle_static，可继续验证 PaddlePaddle 与 GPU 是否可用
import paddle  
print(f"Paddle版本: {paddle.__version__}")
print(f"GPU可用: {paddle.is_compiled_with_cuda()}")
print(f"GPU数量: {paddle.device.cuda.device_count()}")
paddle.utils.run_check()
# # 若使用 transformers 推理引擎，可继续验证 transformers 依赖是否可用
# import transformers
# print(f"Transformers版本: {transformers.__version__}")