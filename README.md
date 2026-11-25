**English** · [한국어](README.ko.md)

# Highlight Research PDF

![A stack of research papers with yellow and green highlights beside an open notebook](docs/images/banner.jpg)

> **My professor wants a literature review. GTA 6 wants my evening.**<br>
> Close the AI chat. The highlights stay in the paper.

## What it does

Give Codex a research paper. The skill picks full sentences from the original text and saves a PDF copy with embedded highlights. Your source PDF stays intact.

| Color | What it marks |
| :--- | :--- |
| 🟨 **Yellow** | The sentence that best captures the point of a substantive paragraph. The highlight has no comment. |
| 🟩 **Green** | Sentences that state a **Problem Statement**, **Research Gap**, **Research Question**, **Methodology**, **Results**, **Contribution to Knowledge**, or **Practical Significance**. The highlight comment carries the matching label or labels. |

If a paragraph's key sentence also serves a research role, it gets a single green highlight.

### Before and after

The same page before and after highlighting. Select either image to see it at full size.

| Before · Original PDF | After · Annotated PDF |
| :---: | :---: |
| [![Page 11 of the paper before annotation](docs/images/before.png)](docs/images/before.png) | [![The same page with yellow takeaways and green research statements](docs/images/after.png)](docs/images/after.png) |

## Read and take notes in Zotero

1. **Highlight.** Ask Codex to highlight the paper and save an annotated PDF copy.
2. **Import.** Attach the copy to the paper's Zotero entry and open it in the Zotero PDF reader. Choose **File → Import Annotations…** to make the highlights editable in Zotero. [Zotero documentation](https://www.zotero.org/support/kb/annotations_in_database#interacting_with_embedded_annotations)
3. **Read with Notes open.** Use the left Annotations pane to jump to a passage and the right Notes pane to write as you read. Drag a highlight into your note to keep a link to the passage. Then write your own take, such as how the authors' evidence supports the claim or where you would use it in your review. [Zotero PDF Reader and Note Editor](https://www.zotero.org/support/pdf_reader)

[![Zotero with the annotation list on the left, the highlighted PDF in the center, and a note open on the right](docs/images/zotero-reading.png)](docs/images/zotero-reading.png)

*A reading setup with annotations on the left, the paper in the middle, and notes on the right.*

## Install in Codex

With Git and Python installed, run these commands in PowerShell, Git Bash, or a macOS/Linux shell. Install PyMuPDF in the Python environment that will run the annotation script.

```sh
git clone https://github.com/giocosogiocondo/highlight-research-pdf.git "$HOME/.agents/skills/highlight-research-pdf"
python -m pip install -r "$HOME/.agents/skills/highlight-research-pdf/requirements.txt"
```

Attach the PDF in Codex and try this prompt.

> Use `$highlight-research-pdf` to highlight this paper and save an annotated PDF copy.

See the [Codex skill documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) for project-scoped installation.

## Apply your own selections

The [annotation script](scripts/annotate.py) takes reviewed excerpts from a PDF with horizontal, selectable text. Use one-based PDF page numbers and exact excerpts in a UTF-8 `selections.json` file. Omit `roles` for yellow, or use the exact English role names above for green.

```json
[
  {"page": 1, "text": "The exact sentence selected from the PDF."},
  {"page": 2, "text": "The exact sentence that states the research gap.", "roles": ["Research Gap"]}
]
```

Run this command from the skill folder.

```sh
python scripts/annotate.py input.pdf selections.json highlighted.pdf
```

Choose a new output filename. For scans and rotated text, see the OCR and layout guidance in [SKILL.md](SKILL.md).

## Screenshot credits

The PDF example uses page 11 of Aleksić, Mandić, and Ivanović (2025), with highlights added in the after and Zotero views. [Paper](https://doi.org/10.3390/educsci15121582) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

The right-hand note in the Zotero screenshot shows figures from Hector Buyones-Gonzalez and Monica Quezada-Espinoza (Universidad Andrés Bello, Chile), presented at the 2024 ASEE Annual Conference & Exposition in Portland, Oregon. © 2024 American Society for Engineering Education. [ASEE paper](https://peer.asee.org/artificial-intelligence-in-the-construction-industry-a-competency-based-examination-through-expert-lens)
