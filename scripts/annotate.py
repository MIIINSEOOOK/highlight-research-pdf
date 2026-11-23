import argparse
import json
import re
import tempfile
import unicodedata
from collections import defaultdict
from pathlib import Path

import pymupdf as fitz


ROLES = {
    "Problem Statement",
    "Research Gap",
    "Research Question",
    "Methodology",
    "Results",
    "Contribution to Knowledge",
    "Practical Significance",
}
YELLOW = (1.0, 0.85, 0.03)
GREEN = (0.23, 0.86, 0.33)


def normalize(text):
    return "".join(
        char for char in unicodedata.normalize("NFKC", text)
        if not char.isspace() and char != "\u00ad"
    )


def index_text(page):
    text = []
    positions = []
    for block in page.get_text("rawdict")["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                for glyph in span["chars"]:
                    chars = normalize(glyph["c"])
                    text.append(chars)
                    position = (line, fitz.Rect(glyph["bbox"]))
                    positions.extend([position] * len(chars))
    return "".join(text), positions


def prepare(doc, records):
    if not isinstance(records, list) or not records:
        raise ValueError("Provide a non-empty array of selections.")
    indexes = {}
    used = defaultdict(list)
    for record in records:
        page_number = record["page"]
        if type(page_number) is not int or not 1 <= page_number <= len(doc):
            raise ValueError(f"Invalid physical PDF page: {page_number!r}")
        excerpt = normalize(record["text"])
        roles = record.get("roles", [])
        if not excerpt or not isinstance(roles, list) or any(role not in ROLES for role in roles):
            raise ValueError(f"Page {page_number}: provide text and valid roles.")
        if page_number not in indexes:
            indexes[page_number] = index_text(doc[page_number - 1])
        text, positions = indexes[page_number]
        matches = list(re.finditer(re.escape(excerpt), text))
        occurrence = record.get("occurrence", 1)
        if (
            type(occurrence) is not int or not 1 <= occurrence <= len(matches)
            or ("occurrence" not in record and len(matches) != 1)
        ):
            raise ValueError(
                f"Page {page_number}: {len(matches)} matches for {record['text'][:100]!r}"
                f" with occurrence {record.get('occurrence')!r}."
            )
        start, end = matches[occurrence - 1].span()
        if any(start < right and left < end for left, right in used[page_number]):
            raise ValueError(f"Page {page_number}: overlapping selections.")
        used[page_number].append((start, end))
        lines = {}
        for line, rect in positions[start:end]:
            if tuple(line["dir"]) != (1.0, 0.0):
                raise ValueError(f"Page {page_number}: selected text needs rotated-text quadrilaterals.")
            key = id(line)
            lines[key] = lines[key] | rect if key in lines else rect
        yield page_number - 1, list(lines.values()), "; ".join(roles)


def annotate(source, selections, output):
    if output.resolve() == source.resolve() or output.exists():
        raise ValueError("Choose a new output path to preserve the source and existing files.")
    records = json.loads(selections.read_text(encoding="utf-8-sig"))
    with fitz.open(source) as doc:
        marks = list(prepare(doc, records))
        expected = []
        for page_index, rects, label in marks:
            page = doc[page_index]
            annotation = page.add_highlight_annot(rects)
            annotation.set_colors(stroke=GREEN if label else YELLOW)
            annotation.set_info(content=label, subject=label)
            annotation.update(opacity=0.40)
            expected.append((page_index, annotation.info["id"], label))

        with tempfile.TemporaryDirectory(dir=output.parent) as temp:
            candidate = Path(temp) / "annotated.pdf"
            doc.save(candidate, garbage=3, deflate=True)
            with fitz.open(candidate) as result:
                assert len(result) == len(doc)
                for page_index, annotation_id, label in expected:
                    page = result[page_index]
                    annotation = page.load_annot(annotation_id)
                    assert annotation.type[0] == fitz.PDF_ANNOT_HIGHLIGHT
                    assert annotation.info["content"] == annotation.info["subject"] == label
            candidate.rename(output)
    print(f"Added {len(marks)} highlight annotations to {output}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply reviewed sentence highlights to a PDF copy.")
    parser.add_argument("source", type=Path)
    parser.add_argument("selections", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    annotate(args.source, args.selections, args.output)
