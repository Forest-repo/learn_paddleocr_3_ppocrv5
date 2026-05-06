"""Save PaddleOCR PP-OCRv5 inference result as CSV.

The script supports the common PaddleOCR 3.x JSON shape. If your installed
version returns extra fields, they will remain in the JSON output from the
other examples; this CSV keeps the high-value fields only.
"""

from __future__ import annotations

import argparse
import csv
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


def extract_rows(payload: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    pages = payload if isinstance(payload, list) else [payload]

    for page_index, page in enumerate(pages):
        if isinstance(page, dict) and "res" in page and isinstance(page["res"], dict):
            res = page["res"]
        elif isinstance(page, dict):
            res = page
        else:
            continue

        texts = res.get("rec_texts") or res.get("texts") or []
        scores = res.get("rec_scores") or res.get("scores") or []
        boxes = res.get("dt_polys") or res.get("rec_boxes") or res.get("boxes") or []

        for index, text in enumerate(texts):
            rows.append(
                {
                    "page_index": page_index,
                    "line_index": index,
                    "text": text,
                    "score": scores[index] if index < len(scores) else "",
                    "box": boxes[index] if index < len(boxes) else "",
                }
            )

    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--output", default="outputs/ocr_result.csv")
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
    payload = to_builtin(ocr.predict(args.image))
    rows = extract_rows(payload)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=["page_index", "line_index", "text", "score", "box"])
        writer.writeheader()
        writer.writerows(rows)

    print(output)


if __name__ == "__main__":
    main()

