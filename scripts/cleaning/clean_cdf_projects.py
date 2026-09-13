"""Turn the raw CDF OCR fragments into one row per council project."""

from __future__ import annotations

import argparse
import csv
import re
import statistics
from dataclasses import dataclass
from datetime import date
from difflib import SequenceMatcher
from pathlib import Path


# Use these paths unless they are overridden on the command line.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUTS = (
    PROJECT_ROOT / "data" / "raw" / "cdf_projects" / "raw_cdf_projects.csv",
    PROJECT_ROOT / "raw_cdf_data.csv",  # legacy OCR output
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "db-unza26-csc4792-kalomo_town_council_cdf_projects.csv"
)

SOURCE_URLS = {
    "Dundumwezi": "https://www.kalomocouncil.gov.zm/?page_id=3025",
    "Kalomo Central": "https://www.kalomocouncil.gov.zm/?page_id=3020",
}

# Each entry is one complete list for a constituency and year.
SOURCES = {
    "CDF-DUNDUMWEZI-2024.pdf": ("Dundumwezi", "2024", "approved_2024"),
    "CDF-KALOMO-CENTRAL-2024.pdf": ("Kalomo Central", "2024", "approved_2024"),
    "2025-DUNDUMWEZI-APPROVED-AND-NOT-APPROVED-PROJECTS.pdf": (
        "Dundumwezi",
        "2025",
        "mixed_2025",
    ),
    "2025-KALOMO-CENTRAL-NOT-APPROVED-AND-APPROVED-PROJECTS.pdf": (
        "Kalomo Central",
        "2025",
        "mixed_2025",
    ),
}

# Known labels help match ward and sector names affected by OCR errors.
WARDS = (
    "All Wards",
    "Bbilili",
    "Chamuka",
    "Chawila",
    "Chifusa",
    "Chikanta",
    "Chilesha",
    "Choonga",
    "Kalonda",
    "Kasuku",
    "Kasukwe",
    "Katanda",
    "Maala",
    "Mayoba",
    "Mikata",
    "Mwaata",
    "Nachikungu",
    "Naluja",
    "Namwianga",
    "Omba",
    "Siachitema",
    "Simayakwe",
    "Sipatunyana",
)

SECTORS = (
    "Agriculture",
    "Commerce and Trade",
    "Education",
    "Energy",
    "Health",
    "Home Affairs",
    "Livestock",
    "Road Infrastructure",
    "Security",
    "Traditional Affairs",
    "Transport",
    "Veterinary",
    "Water and Sanitation",
    "Water Infrastructure",
    "Water Resources",
)

# These headings must not become part of a project name.
HEADER_FRAGMENTS = {
    "comments",
    "name of project",
    "no",
    "project description",
    "project name",
    "reason",
    "sector",
    "sin",
    "type",
    "type of project",
    "ward",
}

# These rejection reasons must not become part of a project name.
REASON_FRAGMENTS = (
    "insufficient funds",
    "insufficeent funds",
    "nsuffice",
    "duplicate",
    "not cdf",
    "not eligible",
    "outside cdf",
    "na",
    "n/a",
)

# These words usually mark the start of a project description.
DESCRIPTION_STARTS = (
    "additional fund",
    "completion",
    "construction",
    "drilling",
    "equipping",
    "fabrication",
    "installation",
    "procurement",
    "purchase",
    "rehabilitation",
    "renovation",
    "supply",
)

# Keep the output columns in the order set by the data dictionary.
OUTPUT_COLUMNS = (
    "project_id",
    "project_name",
    "ward",
    "sector",
    "amount_allocated_zmw",
    "amount_disbursed_zmw",
    "fiscal_year",
    "status",
    "source_url",
    "date_scraped",
)


# Store each OCR fragment with its position on the page.
@dataclass
class OCRLine:
    text: str
    source_file_name: str
    page_number: int
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @property
    def y_center(self) -> float:
        # The centre gives a consistent point for matching fragments to rows.
        return (self.y_min + self.y_max) / 2


# Normalise OCR text before comparing labels.
def normalized(value: str) -> str:
    value = value.upper().replace("|", "I")
    value = re.sub(r"[^A-Z0-9&'()/-]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def compact(value: str) -> str:
    return re.sub(r"[^A-Z]", "", value.upper())


def fuzzy_choice(value: str, choices: tuple[str, ...], threshold: float = 0.76) -> str | None:
    """Match noisy OCR text to the closest expected label."""
    # Return the closest label only when the score is high enough.
    needle = normalized(value)
    best: tuple[float, str] = (0.0, "")
    for choice in choices:
        score = SequenceMatcher(None, needle, normalized(choice)).ratio()
        if score > best[0]:
            best = (score, choice)
    return best[1] if best[0] >= threshold else None


def classify_status(value: str) -> str | None:
    # Check exact text before allowing for OCR spelling errors.
    token = compact(value)
    if token == "APPROVED":
        return "Approved"
    if SequenceMatcher(None, token, "NOTAPPROVED").ratio() >= 0.78:
        return "Not Approved"
    if SequenceMatcher(None, token, "APPROVED").ratio() >= 0.82:
        return "Approved"
    if "APPROVED" not in token:
        return None
    # OCR sometimes misreads the word "NOT" before "APPROVED".
    prefix = token.removesuffix("APPROVED")
    if prefix and SequenceMatcher(None, prefix[-4:], "NOT").ratio() >= 0.55:
        return "Not Approved"
    return "Not Approved"


def clean_fragment(value: str) -> str:
    # Remove row numbers that OCR sometimes joins to the project name.
    value = re.sub(r"^\s*[\[|]?\d{1,3}[OIL]?[\].:-]?\s*", "", value)
    value = re.sub(r"\s+", " ", value).strip(" []|;:-")

    # Remove rejection wording that occasionally spills into the name cell.
    words = value.split()
    if words and SequenceMatcher(None, normalized(words[0]), "INSUFFICIENT").ratio() >= 0.55:
        words = words[1:]
        if words and SequenceMatcher(None, normalized(words[0]), "FUNDS").ratio() >= 0.55:
            words = words[1:]
        value = " ".join(words)
    return value


def is_noise(value: str) -> bool:
    # Remove headings, row numbers, stamps and council letterhead text.
    n = normalized(value).lower()
    if not n or n in HEADER_FRAGMENTS:
        return True
    if re.fullmatch(r"\d{1,4}", n):
        return True
    if any(part in n for part in ("ministry of local", "kalomo town council", "council secretary", "p o box")):
        return True
    return False


def is_reason(value: str) -> bool:
    # Reasons such as "insufficient funds" are not part of a project name.
    n = normalized(value).lower()
    return n in REASON_FRAGMENTS or any(
        n.startswith(prefix)
        for prefix in ("insufficient", "insufficeent", "nsuffice", "duplicate project")
    )


def find_ward(lines: list[str]) -> tuple[str, int | None]:
    """Find and standardise a ward name within a group of OCR fragments."""
    # Search backwards because the ward column is near the end of each row.
    for index in range(len(lines) - 1, -1, -1):
        n = normalized(lines[index])
        ward_aliases = {
            "MILUJA": "Naluja",
            "MWATA": "Mwaata",
            "SIMAYAKWEA": "Simayakwe",
        }
        if n in ward_aliases:
            return ward_aliases[n], index
        for ward in WARDS:
            if re.search(rf"\b{re.escape(normalized(ward))}\b", n):
                return ward, index
        candidate = fuzzy_choice(lines[index], WARDS, 0.70)
        if candidate:
            return candidate, index
        if "ALL WARD" in n or "AIL WARD" in n or "AII WARD" in n:
            return "All Wards", index
    return "N/A", None


def classify_sector(value: str) -> str | None:
    """Return a standard sector name when the OCR text is recognisable."""
    # Handle the sector spellings that appeared most often in the OCR output.
    n = normalized(value)
    token = compact(value)
    aliases = {
        "WATER": "Water and Sanitation",
        "WATER SANITATION": "Water and Sanitation",
        "SANITATION": "Water and Sanitation",
        "ROAD INFRASTUCTURE": "Road Infrastructure",
        "TRADITIONAL AFFFARIRS": "Traditional Affairs",
        "EDUCATION": "Education",
        "EDUACTION": "Education",
        "HEALTH": "Health",
    }
    if n in aliases:
        return aliases[n]
    for sector in SECTORS:
        if n == normalized(sector):
            return sector
    # Check partial words when OCR joined a sector to nearby text.
    compact_markers = (
        ("TRADITIONALAFFA", "Traditional Affairs"),
        ("ROADINFRA", "Road Infrastructure"),
        ("INFRAST", "Infrastructure"),
        ("NSTRAST", "Infrastructure"),
        ("EDUCATION", "Education"),
        ("SANITATION", "Water and Sanitation"),
        ("LIVESTOCK", "Livestock"),
        ("AGRICULTURE", "Agriculture"),
        ("COMMERCE", "Commerce and Trade"),
        ("VETERINARY", "Veterinary"),
        ("TRANSPORT", "Transport"),
        ("DEFENCE", "Defence"),
        ("AESROCK", "Livestock"),
        ("SECURITY", "Security"),
        ("HEALTH", "Health"),
        ("ENERGY", "Energy"),
    )
    for marker, sector in compact_markers:
        if marker in token:
            return sector
    if token in {"WATER", "ATER", "MATER", "WATER"} or token.endswith("WATER"):
        return "Water and Sanitation"
    return fuzzy_choice(value, SECTORS, 0.72)


def find_sector(lines: list[str], stop: int | None = None) -> tuple[str, int | None]:
    # Work backwards from the ward because the sector appears just before it.
    end = len(lines) if stop is None else stop
    for index in range(end - 1, -1, -1):
        candidate = classify_sector(lines[index])
        if candidate:
            return candidate, index
    return "N/A", None


def choose_project_name(lines: list[str], sector_index: int | None) -> str:
    # Project names appear before the sector in the older row format.
    candidates = lines[:sector_index] if sector_index is not None else lines
    candidates = [clean_fragment(x) for x in candidates]
    candidates = [x for x in candidates if x and not is_noise(x)]
    candidates = [x for x in candidates if not is_reason(x)]
    if not candidates:
        return "N/A"

    # Stop when a separate project-description phrase begins.
    description_at = None
    for index, value in enumerate(candidates[1:], 1):
        if normalized(value).lower().startswith(DESCRIPTION_STARTS):
            description_at = index
            break
    name_parts = candidates if description_at is None else candidates[:description_at]
    return re.sub(r"\s+", " ", " ".join(name_parts)).strip()


def median_x(lines: list[OCRLine], label: str, fallback: float) -> float:
    """Find the usual horizontal position of a table column."""
    wanted = normalized(label)
    matches = [line.x_min for line in lines if normalized(line.text) == wanted]
    return statistics.median(matches) if matches else fallback


def row_bounds(anchors: list[OCRLine], index: int) -> tuple[float, float]:
    """Estimate a row's top and bottom from the rows beside it."""
    center = anchors[index].y_center
    lower = (
        (anchors[index - 1].y_max + anchors[index].y_min) / 2
        if index
        else center - 180
    )
    upper = (
        (anchors[index].y_max + anchors[index + 1].y_min) / 2
        if index + 1 < len(anchors)
        else anchors[index].y_max + 60
    )
    return lower, upper


def lines_in_cell(
    page_lines: list[OCRLine],
    lower: float,
    upper: float,
    left: float,
    right: float,
    use_name_alignment: bool = False,
) -> list[OCRLine]:
    """Collect OCR fragments inside one estimated table cell."""
    # Sort by line position so wrapped text is joined in reading order.
    return sorted(
        (
            line
            for line in page_lines
            if lower
            <= (line.y_min + 6 if use_name_alignment else line.y_center)
            < upper
            and left <= line.x_min < right
        ),
        key=lambda line: (line.y_center, line.x_min),
    )


def name_row_bounds_from_serial(
    page_lines: list[OCRLine], anchor: OCRLine, width: float
) -> tuple[float, float] | None:
    """Use a nearby row number to separate close project names."""
    serial_pattern = re.compile(r"^\s*[\[|]?\d{1,3}(?:[\]\[|.:-]|\s|[A-Za-z]|$)")
    serials = sorted(
        (
            line
            for line in page_lines
            if 0.105 * width <= line.x_min < 0.16 * width
            and serial_pattern.match(line.text)
        ),
        key=lambda line: line.y_center,
    )
    if not serials:
        return None

    # Match the approval status with the nearest row number.
    nearest_index = min(
        range(len(serials)),
        key=lambda index: abs(serials[index].y_center - anchor.y_center),
    )
    nearest = serials[nearest_index]
    if abs(nearest.y_center - anchor.y_center) > 20:
        return None
    # Use neighbouring row numbers as the row boundaries when possible.
    lower = nearest.y_center - 45
    upper = nearest.y_center + 45
    if nearest_index:
        previous = serials[nearest_index - 1]
        if nearest.y_center - previous.y_center < 120:
            lower = (previous.y_center + nearest.y_center) / 2
    if nearest_index + 1 < len(serials):
        following = serials[nearest_index + 1]
        if following.y_center - nearest.y_center < 120:
            upper = (nearest.y_center + following.y_center) / 2
    return lower, upper


def project_name_from_cell(lines: list[OCRLine], name_right: float | None = None) -> str:
    """Join the usable text fragments from a project-name cell."""
    parts: list[str] = []
    for line in lines:
        value = clean_fragment(line.text)
        if name_right is not None and line.x_max > name_right + 50:
            # Split an OCR box that crosses from the name into the description.
            merged_description = re.search(
                r"\s+[|\[]?(?:CONSTRUCTION|COMPLETION|DRILLING|PROCUREMENT|"
                r"REHABILITATION|RENOVATION|INSTALLATION|FABRICATION|PURCHASE)\b",
                value,
                flags=re.IGNORECASE,
            )
            if merged_description:
                value = value[: merged_description.start()].strip()
        # Leave headings, reasons and status text out of the project name.
        n = normalized(value)
        if (
            not value
            or is_noise(value)
            or is_reason(value)
            or classify_status(value)
            or len(n) <= 1
        ):
            continue
        parts.append(value)
    return re.sub(r"\s+", " ", " ".join(parts)).strip()


def ward_from_cell(lines: list[OCRLine]) -> str:
    # Try individual fragments before checking a wrapped ward label.
    values = [line.text for line in lines]
    ward, _ = find_ward(values)
    if ward != "N/A":
        return ward
    joined = " ".join(values)
    if re.search(r"A[IL1]{1,2}\s+WARDS?", normalized(joined)):
        return "All Wards"
    return "N/A"


def sector_from_cell(lines: list[OCRLine]) -> str:
    # A sector may be one fragment or several OCR fragments joined together.
    for line in lines:
        sector = classify_sector(line.text)
        if sector:
            return sector
    joined = " ".join(line.text for line in lines)
    return classify_sector(joined) or "N/A"


def status_from_anchor(
    anchor: OCRLine, page_lines: list[OCRLine], comments_x: float
) -> str:
    # Check nearby fragments in case OCR split "NOT APPROVED" into two boxes.
    status = classify_status(anchor.text) or "N/A"
    if status == "Approved":
        companions = [
            compact(line.text)
            for line in page_lines
            if line is not anchor
            and line.x_min >= comments_x - 80
            and abs(line.y_center - anchor.y_center) <= 20
        ]
        if any(
            token in {"NOT", "NOL", "NQT", "NQL", "INOT", "NNOT"}
            for token in companions
        ):
            return "Not Approved"
    return status


def spatial_record(
    name_lines: list[OCRLine],
    ward_lines: list[OCRLine],
    sector_lines: list[OCRLine],
    constituency: str,
    year: str,
    status: str,
    source_file: str,
    name_right: float | None = None,
    fallback_name_lines: list[OCRLine] | None = None,
    all_row_lines: list[OCRLine] | None = None,
) -> dict[str, str]:
    """Build one output record from the reconstructed table cells."""
    # Use the description as a fallback when the name cell is blank.
    project_name = project_name_from_cell(name_lines, name_right)
    if not project_name and fallback_name_lines:
        # Continued rows sometimes have only a description on the next page.
        project_name = project_name_from_cell(fallback_name_lines)
    # Search the full row if OCR placed a ward or sector outside its column.
    sector = sector_from_cell(sector_lines)
    if sector == "N/A" and all_row_lines:
        sector = sector_from_cell(all_row_lines)
    ward = ward_from_cell(ward_lines)
    if ward == "N/A" and all_row_lines:
        ward = ward_from_cell(all_row_lines)
    return {
        "project_id": "",
        "project_name": project_name.title() if project_name else "N/A",
        "ward": ward,
        "sector": sector,
        "amount_allocated_zmw": "N/A",
        "amount_disbursed_zmw": "N/A",
        "fiscal_year": year,
        "status": status,
        "source_url": SOURCE_URLS[constituency],
        "date_scraped": date.today().isoformat(),
        "_constituency": constituency,
        "_source_file": source_file,
    }


def make_record(
    lines: list[str], constituency: str, year: str, status: str, source_file: str
) -> dict[str, str] | None:
    # Build a record from a group of text fragments that already form one row.
    values = [x.strip() for x in lines if x.strip() and not is_noise(x)]
    ward, ward_index = find_ward(values)
    sector, sector_index = find_sector(values, ward_index)
    project_name = choose_project_name(values, sector_index)
    if project_name == "N/A" or len(project_name) < 3:
        return None
    return {
        "project_id": "",
        "project_name": project_name.title(),
        "ward": ward,
        "sector": sector,
        "amount_allocated_zmw": "N/A",
        "amount_disbursed_zmw": "N/A",
        "fiscal_year": year,
        "status": status,
        "source_url": SOURCE_URLS[constituency],
        "date_scraped": date.today().isoformat(),
        "_constituency": constituency,
        "_source_file": source_file,
    }


def parse_2024(lines: list[OCRLine], constituency: str, source_file: str) -> list[dict[str, str]]:
    """Rebuild 2024 records, using the sector column to locate each row."""
    # Use the headings to locate the project, ward and sector columns.
    width = max(line.x_max for line in lines)
    ward_x = median_x(lines, "WARD", 0.57 * width)
    sector_x = median_x(lines, "SECTOR", 0.77 * width)
    project_left = 0.10 * width
    records: list[dict[str, str]] = []
    for page_number in sorted({line.page_number for line in lines}):
        # A sector entry marks each row in the 2024 layout.
        page_lines = [line for line in lines if line.page_number == page_number]
        anchors = sorted(
            (
                line
                for line in page_lines
                if line.x_min >= sector_x - 100 and classify_sector(line.text)
            ),
            key=lambda line: line.y_center,
        )
        for index, anchor in enumerate(anchors):
            # Sector text sits near the lower edge of each 2024 row.
            lower = anchors[index - 1].y_max if index else anchor.y_center - 180
            upper = anchor.y_max + 6
            records.append(
                spatial_record(
                    lines_in_cell(page_lines, lower, upper, project_left, ward_x - 20),
                    lines_in_cell(page_lines, lower, upper, ward_x - 80, sector_x - 20),
                    [anchor],
                    constituency,
                    "2024",
                    "Approved",
                    source_file,
                )
            )
    return records


def parse_2025(lines: list[OCRLine], constituency: str, source_file: str) -> list[dict[str, str]]:
    """Rebuild 2025 records, using approval status to locate each row."""
    # Use repeated headings to locate each column.
    width = max(line.x_max for line in lines)
    description_x = median_x(
        lines,
        "PROJECT DESCRIPTION",
        0.42 * width if constituency == "Dundumwezi" else 0.30 * width,
    )
    sector_x = median_x(lines, "SECTOR", 0.59 * width)
    type_x = median_x(lines, "TYPE", median_x(lines, "TYPE OF PROJECT", 0.68 * width))
    ward_x = median_x(lines, "WARD", 0.75 * width)
    comments_x = median_x(lines, "COMMENTS", 0.81 * width)
    project_left = 0.10 * width
    records: list[dict[str, str]] = []
    for page_number in sorted({line.page_number for line in lines}):
        # An approval status marks each row in the 2025 layout.
        page_lines = [line for line in lines if line.page_number == page_number]
        anchors = sorted(
            (
                line
                for line in page_lines
                if line.x_min >= 0.72 * width and classify_status(line.text)
            ),
            key=lambda line: line.y_center,
        )
        for index, anchor in enumerate(anchors):
            # Estimate the row's top and bottom before reading its cells.
            lower, upper = row_bounds(anchors, index)
            row_lines = [
                line for line in page_lines if lower <= line.y_center < upper
            ]
            # Dundumwezi row numbers separate names that sit close together.
            name_lower, name_upper = lower, upper
            serial_bounds = (
                name_row_bounds_from_serial(page_lines, anchor, width)
                if constituency == "Dundumwezi"
                else None
            )
            if serial_bounds:
                # Tighten the range to the neighbouring row numbers.
                name_lower = max(serial_bounds[0], lower - 15)
                name_upper = min(serial_bounds[1], upper + 3)
            # Read the name and description areas separately.
            name_lines = lines_in_cell(
                page_lines,
                name_lower,
                name_upper,
                project_left,
                description_x - 10,
                use_name_alignment=(
                    constituency == "Dundumwezi" and serial_bounds is None
                ),
            )
            description_lines = lines_in_cell(
                page_lines, lower, upper, description_x - 80, sector_x - 10
            )
            # Build one output record from the recovered cells.
            records.append(
                spatial_record(
                    name_lines,
                    lines_in_cell(
                        page_lines,
                        lower - 5,
                        upper + 5,
                        ward_x - 80,
                        comments_x - 10,
                    ),
                    lines_in_cell(page_lines, lower, upper, sector_x - 80, type_x - 10),
                    constituency,
                    "2025",
                    status_from_anchor(anchor, page_lines, comments_x),
                    source_file,
                    description_x - 10,
                    description_lines,
                    row_lines,
                )
            )
    return records


def load_ocr(path: Path) -> list[OCRLine]:
    """Load the raw OCR file and check that its position columns exist."""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)

        # The cleaner cannot rebuild table rows without these coordinates.
        required = {
            "text_line",
            "source_file_name",
            "page_number",
            "x_min",
            "y_min",
            "x_max",
            "y_max",
        }
        if not required.issubset(reader.fieldnames or ()):
            raise ValueError(f"{path} must contain columns: {sorted(required)}")
        return [
            OCRLine(
                text=row["text_line"].strip(),
                source_file_name=Path(row["source_file_name"]).name,
                page_number=int(row["page_number"]),
                x_min=float(row["x_min"]),
                y_min=float(row["y_min"]),
                x_max=float(row["x_max"]),
                y_max=float(row["y_max"]),
            )
            for row in reader
            if row["text_line"].strip()
        ]


def select_input(requested: str | None) -> Path:
    # Prefer an explicit path, then try the standard and older locations.
    if requested:
        return Path(requested).resolve()
    for candidate in DEFAULT_INPUTS:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("No CDF OCR input found in the standard or legacy location")


def deduplicate(records: list[dict[str, str]]) -> list[dict[str, str]]:
    # Compare the identifying fields while preserving the first occurrence.
    output: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    for record in records:
        key = (
            record["_constituency"],
            record["fiscal_year"],
            normalized(record["project_name"]),
            normalized(record["ward"]),
            record["status"],
        )
        if key not in seen:
            seen.add(key)
            output.append(record)
    return output


def validate(records: list[dict[str, str]]) -> None:
    """Stop the export if obvious invalid data or personal IDs are found."""
    if not records:
        raise ValueError("No project records were reconstructed")
    for record in records:
        # Project names should not be numbers, NRCs or phone numbers.
        name = record["project_name"]
        if re.fullmatch(r"[\d\s,./|-]+", name):
            raise ValueError(f"Numeric-only project name detected: {name!r}")
        if re.search(r"\b\d{5,7}/\d{2}/\d\b", name):
            raise ValueError(f"Possible NRC detected in project name: {name!r}")
        if re.fullmatch(r"0?9\d{8}", re.sub(r"\D", "", name)):
            raise ValueError(f"Possible phone number detected in project name: {name!r}")


def clean_cdf_data(input_path: Path, output_path: Path) -> list[dict[str, str]]:
    """Parse the four sources and write the final pipe-separated dataset."""
    # Group fragments by PDF so each layout is handled independently.
    rows = load_ocr(input_path)
    grouped: dict[str, list[OCRLine]] = {name: [] for name in SOURCES}
    for row in rows:
        if row.source_file_name in grouped:
            grouped[row.source_file_name].append(row)

    # All four selected PDFs are required for the complete dataset.
    missing = [name for name, values in grouped.items() if not values]
    if missing:
        raise ValueError(f"Canonical project sources missing from OCR input: {missing}")

    # Use the parser that matches the source table's year.
    records: list[dict[str, str]] = []
    for source_file, (constituency, _, parser_name) in SOURCES.items():
        source_lines = grouped[source_file]
        if parser_name == "approved_2024":
            records.extend(parse_2024(source_lines, constituency, source_file))
        else:
            records.extend(parse_2025(source_lines, constituency, source_file))

    # Keep repeated names because they can be separate applications.
    for index, record in enumerate(records, 1):
        record["project_id"] = f"CDF-{index:04d}"

    # Check the records before writing the pipe-separated file.
    validate(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_COLUMNS, delimiter="|", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    return records


def main() -> None:
    """Read command-line paths and run the cleaning process."""
    # Optional paths are useful for local tests and Colab runs.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="OCR CSV path (defaults to standard path, then legacy root file)")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Processed pipe-delimited CSV path")
    args = parser.parse_args()

    input_path = select_input(args.input)
    output_path = Path(args.output).resolve()
    records = clean_cdf_data(input_path, output_path)
    by_year = {year: sum(r["fiscal_year"] == year for r in records) for year in ("2024", "2025")}
    print(f"Read OCR fragments from {input_path}")
    print(f"Saved {len(records)} project records to {output_path}")
    print(f"Records by year: {by_year}")


if __name__ == "__main__":
    main()
