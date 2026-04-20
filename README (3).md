# The Cursed PDF Pack

Four deliberately evil PDFs for the RAG Bootcamp (Day 2 onward).
Each breaks a different class of naive document parser. Hand these to
teams and watch their Day 1 pipelines disintegrate.

---

## 01_multipage_table_of_doom.pdf
**Content:** 4-page Q2 inventory valuation report for a fake industrial supplier.

**Evil features:**
- Table spans all 4 pages with column headers repeated on each page (naive extractors will count the header row 4 times)
- Each page has a "Subtotal (page X of N)" row that **looks like a real data row** but is derived — teams must detect and skip it
- Multi-line "Description" and "Notes" columns test wrap handling
- "Running total through page X" footers pollute the text layer
- The first grand total appears only on page 4

**What to teach with it:**
- Why `pdfplumber.extract_tables()` returns 4 tables (one per page) instead of 1 logical table
- How to reconstruct a cross-page table by detecting repeated headers and subtotal rows
- When to reach for layout-aware tools (Docling, Unstructured) vs. table-specialist tools (Camelot)

---

## 02_nested_bullet_nightmare.pdf
**Content:** SOP-QA-2024-017 "Incoming Material Inspection" — 3 pages of deeply nested procedures.

**Evil features:**
- 4 levels of nested indentation: Roman (I, II, III) → Caps (A, B) → Numeric (1, 2) → Alpha (a, b, c)
- Bullets that span a page break mid-hierarchy (page 2 starts mid-list **without** repeating the parent context)
- Paragraphs interspersed among bullets, not just one-line items
- Different section ("3. Nonconformance Handling") uses flat numeric bullets, so parsers can't assume one consistent scheme

**What to teach with it:**
- Why flat text extraction loses the hierarchy entirely — "a. Surface finish per drawing callout" is meaningless without knowing it sits under "1. Visual inspection checklist" under "A. Visual and Dimensional Inspection" under "I. Class A — Critical Components"
- Layout-aware parsers can recover this from indentation + font
- How to encode the hierarchy in chunk metadata (`parent_section`, `list_level`) so retrieval can bring the full context back

---

## 03_layout_monster.pdf
**Content:** Fake "Acme Quarterly" corporate newsletter, 2 pages in 2-column layout.

**Evil features:**
- 2-column article flow — naive `pdftotext` reads left-to-right across both columns and scrambles sentences
- Blue-boxed sidebar ("AT A GLANCE") with bullet points that interrupt the main article
- Pull quotes in large italic that appear mid-article
- Repeating header bar and footer on every page (polluting text layer)
- Multiple articles across the 2 pages with different authors

**What to teach with it:**
- Why `pdftotext` without `-layout` destroys this document
- Why `pdftotext -layout` partially helps but still struggles
- How layout-aware parsers (Docling, Unstructured) detect reading order via bounding boxes
- How to strip repeating header/footer text before chunking

---

## 04_skewed_scan.pdf
**Content:** 3-page Master Services Agreement, rendered as images (no text layer).

**Evil features:**
- Each page rotated 2.5–3.8° in alternating directions (phone-scan skew)
- JPEG compression at quality 72 (mimicking typical scanner app output)
- Warm paper tint + added noise + gaussian blur
- Vignetting on page edges
- Random brown smudge blobs on some pages
- **No text layer at all** — OCR is the only way in

**What to teach with it:**
- Detecting that a PDF has no text layer (`pdfplumber.extract_text()` returns empty)
- OCR with Tesseract — and why it fails badly on non-deskewed pages
- Deskewing with OpenCV (Hough transform or minAreaRect on binarized image)
- The word error rate delta between pre- and post-deskew OCR — often 30%+ of words recovered

**Note on authenticity:** This is programmatically generated to *look* like a scan. Real scanner output has additional artifacts (irregular lighting, paper texture, binder holes, handwritten marks) that are hard to simulate fully. If you can, supplement with one genuinely scanned document you print and re-scan yourself on a phone. Treat this file as a baseline — if a team can't OCR this cleanly, they're not ready for real client scans.

---

## Using the pack

- **Day 2 morning, 09:00:** hand teams the pack. Have them run yesterday's Day 1 pipeline on it. Document what breaks.
- **Day 2 afternoon:** teams pick tools and rebuild parsing. Target: a `parse_pdf(path) -> List[Element]` function that handles all 4 files.
- **Day 3:** the parsed Elements from these PDFs feed the chunking + metadata exercises. No new parsing work.
- **Day 5:** keep the pack as a validation set. Teams point their final capstone pipeline at it and report any regressions.
