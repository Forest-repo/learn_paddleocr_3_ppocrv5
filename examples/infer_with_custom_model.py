"""Run inference with exported/custom PaddleOCR models.

Use this after training and exporting detection/recognition models.

Example:
    python examples/infer_with_custom_model.py ^
      --image images/test.jpg ^
      --det-model-dir output/det_export ^
      --rec-model-dir output/rec_export
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paddleocr import PaddleOCR


def to_builtin(value: Any) -> Any:
    if hasattr(value, "json"):
        data = value.json
        return data() if callable(data) else data
    if hasattr(value, "to_json"):
        return value.to_json()
    if isinstance(value, dict):
        return {key: to_builtin(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_builtin(item) for item in value]
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="费用组-单票-商业发票-007.png")
    parser.add_argument("--det-model-dir", default="output/det_export")
    parser.add_argument("--rec-model-dir", default="output/rec_export")
    parser.add_argument(
        "--rec-char-dict-path",
        help=(
            "Optional note-only argument. PaddleOCR 3.x usually reads the exported "
            "recognition postprocess/dictionary settings from inference.yml."
        ),
    )
    parser.add_argument("--output", default="outputs/custom_model_result.json")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    ocr = PaddleOCR(
        ocr_version="PP-OCRv5",
        lang="ch",
        device=args.device,
        text_detection_model_dir=args.det_model_dir,
        text_recognition_model_dir=args.rec_model_dir,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )

    payload = to_builtin(ocr.predict(args.image))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.rec_char_dict_path:
        print(
            "Note: --rec-char-dict-path is kept for workflow clarity. "
            "For PaddleOCR 3.x, verify the exported rec model directory contains inference.yml "
            "with the same dictionary/postprocess settings used during training."
        )
    print(output)


if __name__ == "__main__":
    main()
