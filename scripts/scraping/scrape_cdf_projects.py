"""Extract CDF project tables from the scanned council PDFs using OCR."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


# Use these paths unless they are overridden on the command line.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PDF_DIR = PROJECT_ROOT / "Dataset"
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "raw" / "cdf_projects" / "raw_cdf_projects.csv"

# These four combined lists cover both constituencies without duplicate sources.
CANONICAL_PROJECT_PDFS = (
    "CDF-DUNDUMWEZI-2024.pdf",
    "CDF-KALOMO-CENTRAL-2024.pdf",
    "2025-DUNDUMWEZI-APPROVED-AND-NOT-APPROVED-PROJECTS.pdf",
    "2025-KALOMO-CENTRAL-NOT-APPROVED-AND-APPROVED-PROJECTS.pdf",
)

# Save the text, page, position and confidence for each OCR result.
OUTPUT_COLUMNS = (
    "text_line",
    "source_file_name",
    "page_number",
    "x_min",
    "y_min",
    "x_max",
    "y_max",
    "ocr_confidence",
)


def extract_scanned_pdf_data(pdf_dir: Path, output_file: Path, gpu: bool) -> int:
    """Run OCR on the selected PDFs and save every detected text fragment."""
    # Load OCR packages only when extraction starts.
    try:
        import easyocr
        import numpy as np
        import pypdfium2 as pdfium
    except ImportError as exc:
        raise SystemExit(
            "CDF OCR dependencies are missing. Install easyocr, numpy, and "
            "pypdfium2 in the environment used for extraction."
        ) from exc

    # Stop early if any selected PDF is missing.
    missing = [name for name in CANONICAL_PROJECT_PDFS if not (pdf_dir / name).exists()]
    if missing:
        raise FileNotFoundError(f"Missing selected CDF project PDFs: {missing}")

    print(f"Initializing EasyOCR (GPU={gpu})")
    reader = easyocr.Reader(["en"], gpu=gpu)
    extracted: list[dict[str, object]] = []

    # OCR one page at a time and keep each text box's position.
    for file_name in CANONICAL_PROJECT_PDFS:
        file_path = pdf_dir / file_name
        print(f"Processing {file_name}")
        pdf = pdfium.PdfDocument(str(file_path))
        try:
            for page_index, page in enumerate(pdf):
                # The higher resolution helps EasyOCR read small table text.
                image = page.render(scale=300 / 72).to_pil()
                results = reader.readtext(np.asarray(image), detail=1, paragraph=False)
                for box, text, confidence in results:
                    # Skip empty detections.
                    cleaned = str(text).strip()
                    if not cleaned:
                        continue
                    xs = [float(point[0]) for point in box]
                    ys = [float(point[1]) for point in box]
                    extracted.append(
                        {
                            "text_line": cleaned,
                            "source_file_name": file_name,
                            "page_number": page_index + 1,
                            "x_min": round(min(xs), 2),
                            "y_min": round(min(ys), 2),
                            "x_max": round(max(xs), 2),
                            "y_max": round(max(ys), 2),
                            "ocr_confidence": round(float(confidence), 5),
                        }
                    )
        finally:
            pdf.close()

    # Keep the fragments in their original reading order.
    extracted.sort(
        key=lambda row: (
            str(row["source_file_name"]),
            int(row["page_number"]),
            float(row["y_min"]),
            float(row["x_min"]),
        )
    )

    # Each OCR text box becomes one row in the raw CSV.
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(extracted)

    print(f"Saved {len(extracted)} OCR fragments to {output_file}")
    return len(extracted)


def main() -> None:
    """Read command-line options and start the OCR extraction."""
    # Path options allow the same script to run locally or in Colab.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", default=str(DEFAULT_PDF_DIR))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument(
        "--gpu",
        action="store_true",
        help="Use EasyOCR GPU acceleration (CPU is the safe default)",
    )
    args = parser.parse_args()
    extract_scanned_pdf_data(Path(args.pdf_dir), Path(args.output), args.gpu)


if __name__ == "__main__":
    main()
