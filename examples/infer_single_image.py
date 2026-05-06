"""Run PaddleOCR PP-OCRv5 inference on one image.

Example:
    python examples/infer_single_image.py --image assets/demo.jpg --device cpu
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paddleocr import PaddleOCR


def build_ocr(args: argparse.Namespace) -> PaddleOCR:
    kwargs: dict[str, Any] = {
        "ocr_version": "PP-OCRv5",
        "lang": args.lang,
        "device": args.device,
        "use_doc_orientation_classify": False,
        "use_doc_unwarping": False,
        "use_textline_orientation": args.use_textline_orientation,
    }

    if args.model_size == "mobile":
        kwargs.update(
            {
                "text_detection_model_name": "PP-OCRv5_mobile_det",
                "text_recognition_model_name": "PP-OCRv5_mobile_rec",
            }
        )
    elif args.model_size == "server":
        kwargs.update(
            {
                "text_detection_model_name": "PP-OCRv5_server_det",
                "text_recognition_model_name": "PP-OCRv5_server_rec",
            }
        )

    return PaddleOCR(**kwargs)


def result_to_builtin(result: Any) -> Any:
    """Convert PaddleOCR result objects to JSON-serializable Python objects."""
    if hasattr(result, "json"):
        data = result.json
        return data() if callable(data) else data
    if hasattr(result, "to_json"):
        return result.to_json()
    if isinstance(result, (list, tuple)):
        return [result_to_builtin(item) for item in result]
    if isinstance(result, dict):
        return {key: result_to_builtin(value) for key, value in result.items()}
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Path to input image.")
    parser.add_argument("--device", default="cpu", help="cpu, gpu, gpu:0, etc.")
    parser.add_argument("--lang", default="ch", help="Recognition language, e.g. ch/en.")
    parser.add_argument(
        "--model-size",
        choices=["default", "mobile", "server"],
        default="default",
        help="default lets PaddleOCR choose the PP-OCRv5 default pipeline.",
    )
    parser.add_argument(
        "--use-textline-orientation",
        action="store_true",
        help="Enable text line orientation classification for rotated text.",
    )
    parser.add_argument("--json-out", help="Optional JSON output path.")
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    ocr = build_ocr(args)
    results = ocr.predict(str(image_path))
    payload = result_to_builtin(results)

    print(json.dumps(payload, ensure_ascii=False, indent=2))

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Saved JSON to {out_path}")


if __name__ == "__main__":
    main()

