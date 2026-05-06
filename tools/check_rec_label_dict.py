"""Check whether recognition labels are covered by a PaddleOCR dict file.

Example:
    python tools/check_rec_label_dict.py ^
      --label-file datasets/rec_dataset_template/train.txt ^
      --dict-file datasets/rec_dataset_template/dict.txt
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path


def load_dict(path: Path) -> set[str]:
    chars: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line:
            chars.add(line.rstrip("\n"))
    return chars


def iter_labels(path: Path) -> list[tuple[int, str, str]]:
    rows: list[tuple[int, str, str]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        if "\t" not in line:
            raise ValueError(f"Line {line_no} has no tab separator: {line}")
        image_path, label = line.split("\t", 1)
        rows.append((line_no, image_path, label))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label-file", required=True)
    parser.add_argument("--dict-file", required=True)
    parser.add_argument("--use-space-char", action="store_true")
    parser.add_argument("--max-text-length", type=int, default=25)
    args = parser.parse_args()

    label_file = Path(args.label_file)
    dict_file = Path(args.dict_file)
    dict_chars = load_dict(dict_file)
    if args.use_space_char:
        dict_chars.add(" ")

    missing = Counter()
    too_long: list[tuple[int, str, int]] = []

    for line_no, _image_path, label in iter_labels(label_file):
        if len(label) > args.max_text_length:
            too_long.append((line_no, label, len(label)))
        for char in label:
            if char not in dict_chars:
                missing[char] += 1

    print(f"label_file: {label_file}")
    print(f"dict_file: {dict_file}")
    print(f"dict_chars: {len(dict_chars)}")

    if missing:
        print("\nMissing chars:")
        for char, count in missing.most_common():
            visible = "<space>" if char == " " else char
            print(f"  {visible}\t{count}")
    else:
        print("\nMissing chars: none")

    if too_long:
        print(f"\nLabels longer than max_text_length={args.max_text_length}:")
        for line_no, label, length in too_long[:50]:
            print(f"  line {line_no}: length={length}, label={label}")
    else:
        print(f"\nLabels longer than max_text_length={args.max_text_length}: none")


if __name__ == "__main__":
    main()
