"""Save PaddleOCR PP-OCRv5 inference result as JSON.

This script is intentionally tiny so you can copy the core logic into your app.
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
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", default="outputs/ocr_result.json")
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    ocr = PaddleOCR(
        ocr_version="PP-OCRv5",
        lang="ch",
        device=args.device,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )
    result = ocr.predict(args.image)
    payload = to_builtin(result)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()

