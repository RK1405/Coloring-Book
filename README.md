# Kids Coloring Books

Python scripts that generate four 40-page A4 coloring books for kids aged 3–8, ready to upload to Amazon KDP:

| Book | Script |
|---|---|
| Animals | `animals.py` |
| Flowers | `flowers.py` |
| Cars & Motors | `vehicles.py` |
| Household Items | `household.py` |

Each book has 20 cartoon pictures with thick outlines on a clean white background. Every picture is on a right-hand page and the back of each picture is left blank, so markers don't bleed through onto the next picture. Each page shows a small colour reference image, the name in outlined letters, and a large drawing to colour in.

## Setup

```bash
pip install -r requirements.txt
```

The page titles use the Fredoka font (SIL Open Font License, free for commercial use). Install it once:

```bash
mkdir -p ~/.fonts && cp fonts/Fredoka-Bold.ttf ~/.fonts/ && fc-cache -f
```

On Windows or macOS, double-click `fonts/Fredoka-Bold.ttf` and choose Install.

## Build

```bash
python build.py
```

This writes one folder per book under `output/`:

- `<book>_interior_A4.pdf`: the 40-page print-ready interior (210 × 297 mm, 15 mm safe margins)
- `<book>_kindle_cover_1600x2560.jpg`: the Kindle eBook cover

`python print_cover.py` makes the KDP paperback wraparound cover (back, spine and front) for A4 trim at 360 DPI, as PDF, PNG and JPG. The spine width comes from the page count (0.002252 in per page on white paper). The bottom-right of the back is left clear for the barcode Amazon adds. Covers are set up in the `BOOKS` dictionary in that script.
- `png_pages/`: every picture page as a 300 DPI PNG
- `line_art/`: each drawing alone, outline only
- `color_ref/`: each drawing alone, in colour
- `<book>_preview_contact_sheet.png`: all 20 drawings on one sheet

## How the drawings work

Each drawing is a Python function that returns SVG shapes on a 400 × 400 canvas. The helpers live in `lib.py` (`C` circle, `E` ellipse, `R` rectangle, `P` path, `L` line, `eye`, `smile`, and others). Each shape gets a colour name from the palette. The same function renders twice:

- **line mode**: every fill becomes white, which gives the colouring page
- **colour mode**: the palette colours are used, which gives the thumbnail and the covers

To change a book, edit its `BOOK` list at the bottom of the script (title and drawing function), then run `python build.py` again. Keep it at 20 entries for a 40-page book.

The vehicles have their friendly eyes in the headlights and smiles on the bumpers, not in the windscreen, so they stay clearly original. None of them use brands or logos.
