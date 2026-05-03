#!/usr/bin/env python3
"""Duplicate PDF pages and isolate AcroForm fields per copy.

Usage:
  python pdf_page_duplicator.py \
    --input in.pdf --output out.pdf \
    --source-page 3 --copies 5 \
    --field name='John {copy}' --field invoice='INV-{page}-{copy}'
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject


@dataclass(frozen=True)
class DuplicateInstruction:
    source_page_index: int
    copies: int
    field_templates: Dict[str, str]


def _resolve_template(template: str, *, page_number: int, copy_number: int) -> str:
    return template.replace("{page}", str(page_number)).replace("{copy}", str(copy_number))


def _isolate_page_fields(page_obj, *, source_page_index: int, copy_index: int) -> dict[str, str]:
    """Rename annotation field names on this page and return old->new map."""
    remap: dict[str, str] = {}
    annots = page_obj.get("/Annots", [])

    for annot_ref in annots:
        annot = annot_ref.get_object()
        old_name = annot.get("/T")
        if old_name is None:
            continue
        old_name_str = str(old_name)
        new_name = f"{old_name_str}__p{source_page_index + 1}_c{copy_index + 1}"
        annot[NameObject("/T")] = TextStringObject(new_name)
        remap[old_name_str] = new_name

    return remap


def duplicate_pdf(input_path: Path, output_path: Path, instruction: DuplicateInstruction) -> None:
    reader = PdfReader(str(input_path))
    writer = PdfWriter()

    if instruction.source_page_index < 0 or instruction.source_page_index >= len(reader.pages):
        raise ValueError("source_page_index out of range")
    if instruction.copies <= 0:
        raise ValueError("copies must be > 0")

    # Copy original pages.
    for p in reader.pages:
        writer.add_page(p)

    # Duplicate selected page with field name isolation.
    selected = reader.pages[instruction.source_page_index]
    for copy_index in range(instruction.copies):
        writer.add_page(selected)
        target_page = writer.pages[len(writer.pages) - 1]

        remap = _isolate_page_fields(
            target_page,
            source_page_index=instruction.source_page_index,
            copy_index=copy_index,
        )

        values: dict[str, str] = {}
        for original_name, template in instruction.field_templates.items():
            unique_name = remap.get(original_name)
            if unique_name is None:
                continue
            values[unique_name] = _resolve_template(
                template,
                page_number=instruction.source_page_index + 1,
                copy_number=copy_index + 1,
            )

        if values:
            writer.update_page_form_field_values(target_page, values)

    with output_path.open("wb") as fh:
        writer.write(fh)


def _parse_field_pairs(field_pairs: list[str]) -> Dict[str, str]:
    parsed: Dict[str, str] = {}
    for item in field_pairs:
        if "=" not in item:
            raise ValueError(f"Invalid --field '{item}', expected key=value")
        key, value = item.split("=", 1)
        parsed[key.strip()] = value.strip()
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="Duplicate a PDF page and isolate fields per copy")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-page", required=True, type=int, help="0-based page index")
    parser.add_argument("--copies", required=True, type=int)
    parser.add_argument("--field", action="append", default=[], help="field override key=value; supports {page} and {copy}")

    args = parser.parse_args()
    instruction = DuplicateInstruction(
        source_page_index=args.source_page,
        copies=args.copies,
        field_templates=_parse_field_pairs(args.field),
    )
    duplicate_pdf(args.input, args.output, instruction)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
