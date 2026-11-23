# Highlight Research PDF

A Codex skill for reading academic papers and saving an annotated PDF copy. Yellow highlights capture paragraph takeaways. Green highlights label the study’s problem, research gap, questions, methodology, results, contribution, or practical significance. The annotations are embedded in the output PDF for use in PDF readers such as Zotero.

## Install for Codex

Run these commands in PowerShell, Git Bash, or a macOS/Linux shell with Git and Python available.

```sh
git clone https://github.com/giocosogiocondo/highlight-research-pdf.git "$HOME/.agents/skills/highlight-research-pdf"
python -m pip install -r "$HOME/.agents/skills/highlight-research-pdf/requirements.txt"
```

Use the Python environment that will run the annotation script. Attach or reference a paper in Codex and ask:

> Use $highlight-research-pdf to highlight this paper and give me an annotated PDF copy.

See [Codex skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) for repository-scoped installation.

## Run the annotation script directly

The script applies reviewed selections to horizontal, selectable PDF text. Create a UTF-8 `selections.json` file with one-based physical PDF page numbers and exact excerpts from the PDF text layer. Omit `roles` for yellow and supply the role names in [SKILL.md](SKILL.md) for green.

```json
[
  {"page": 1, "text": "Replace this with the exact paragraph takeaway."},
  {"page": 2, "text": "Replace this with the exact research gap sentence.", "roles": ["Research Gap"]}
]
```

From the skill folder, run:

```sh
python scripts/annotate.py input.pdf selections.json highlighted.pdf
```

Choose a new output filename. For scanned papers or rotated text, the [skill instructions](SKILL.md) describe when to use OCR or another layout-specific method.
