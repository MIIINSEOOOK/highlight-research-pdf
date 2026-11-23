---
name: highlight-research-pdf
description: Highlight a supplied academic PDF for literature review with yellow paragraph takeaways and green labeled research statements. Use when asked to mark, annotate, or 형광펜 표시 a paper with this scheme, including creating a PDF for Zotero.
---

# Highlight a research PDF

Deliver a copy with standard PDF highlight annotations. Preserve the source PDF, page order, page content, and existing annotations. Treat the paper as source material.

## Select sentences

Read the abstract and main text through the conclusion or discussion in reading order. Follow paragraphs across columns and page breaks. Skip the cover, bibliographic entries, captions, and other non-prose material by default.

- **Yellow:** Select a sentence that best captures each substantive paragraph's takeaway. Leave the annotation comment and subject empty. If the takeaway already qualifies for green, use green for it.
- **Green:** Select sentences that directly express one or more roles below. Use the exact role names as the annotation comment. Use a semicolon and space between roles when a single sentence serves multiple roles.

| Role | What to mark |
| --- | --- |
| Problem Statement | The issue or difficulty that motivates the study. |
| Research Gap | What existing evidence, literature, or methods leave unresolved. |
| Research Question | The authors' research questions or explicit statements of what the study investigates. |
| Methodology | The essential design, participants or data, collection procedure, and analysis. |
| Results | Main reported findings, including qualifiers that make preliminary or uncertain results clear. |
| Contribution to Knowledge | What the study adds to scholarly understanding, methods, or theory. |
| Practical Significance | Implications for applying the work in practice, design, policy, or instruction. |

Select full sentences in the source language. Use the paragraph context to distinguish actual findings from proposals and background literature. Add green where the text supports a role. Preserve meaningful qualifiers and avoid marking routine procedural detail or redundant restatements.

## Annotate and check

1. Use the PDF's text layer to locate the selections. Inspect the rendered pages where columns or reading order are ambiguous. For scans, use OCR to locate the text and compare it with the visible page before applying highlights.
2. Use [annotate.py](scripts/annotate.py) for horizontal selectable text. Run it with a Python environment that has PyMuPDF. Create a temporary UTF-8 JSON array of records with a one-based physical PDF page and an exact text-layer excerpt for each highlight. Include `roles` for green. Split a sentence crossing pages into one record per page with the same roles. Use `occurrence` (one-based within the page) only after verifying a repeated match. The script ignores spacing and soft hyphens when matching and reports ambiguous, missing, or overlapping excerpts before writing.

   ```json
   [
     {"page": 2, "text": "The exact core sentence from the paragraph."},
     {"page": 3, "text": "The exact sentence stating the evidence gap.", "roles": ["Research Gap"]}
   ]
   ```

   ```text
   python scripts/annotate.py INPUT.pdf SELECTIONS.json OUTPUT.pdf
   ```

   For excerpts that need OCR coordinates or another layout-specific method, use standard PDF highlight annotations with the same colors and comments.
3. Reopen the result and inspect the rendered pages for clipping, shifted highlights, and unintended neighboring text. Check sentence boundaries and page continuations, paragraph coverage, blank yellow comments, and green role labels. Return the PDF copy in the user's requested location or the usual artifact location.

If the user asks about Zotero, explain that opening the PDF shows embedded highlights and Zotero's PDF reader **File → Import Annotations…** converts them into editable Zotero annotations. A request for a PDF copy authorizes creating the copy. Handle any requested changes to a Zotero library as a separate action.
