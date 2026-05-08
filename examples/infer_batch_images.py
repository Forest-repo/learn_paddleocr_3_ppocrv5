"""Run PaddleOCR PP-OCRv5 inference on all images in a directory.

Example:
    python examples/infer_batch_images.py --input-dir images --output-dir outputs/json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paddleocr import PaddleOCR


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def build_ocr(device: str, lang: str) -> PaddleOCR:
    return PaddleOCR(
        ocr_version="PP-OCRv5",
        lang=lang,
        device=device,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )


def result_to_builtin(result: Any) -> Any:
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


def iter_images(input_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default=".")
    parser.add_argument("--output-dir", default="outputs/json")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--lang", default="ch")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    images = iter_images(input_dir)
    if not images:
        raise FileNotFoundError(f"No images found in {input_dir}")

    ocr = build_ocr(args.device, args.lang)
    summary = []

    for image_path in images:
        results = ocr.predict(str(image_path))
        payload = result_to_builtin(results)
        out_path = output_dir / f"{image_path.stem}.json"
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        summary.append({"image": str(image_path), "json": str(out_path)})
        print(f"OK {image_path} -> {out_path}")

    (output_dir / "_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

