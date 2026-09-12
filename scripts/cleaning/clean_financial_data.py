"""
clean_financial_data.py

Takes the raw scraped text (from scrape_financial_html.py,
scrape_financial_pdfs.py, and/or crawl_and_scrape_financial.py) and
turns it into one clean, structured table of financial and revenue
records for Kalomo Town Council.

This script demonstrates the two things markers look for:
  1. Extraction  -> turning messy prose/tables into structured rows
  2. Cleaning    -> normalising numbers, dates, removing symbols

Usage:
    python3 scripts/cleaning/clean_financial_data.py
"""

import re
import csv
import sys
from pathlib import Path

import pandas as pd

# Some scraped PDFs (e.g. a full Integrated Development Plan) produce a
# single text field far larger than Python's default 128KB CSV limit.
# Raise it so those rows can still be read instead of crashing. Some
# platforms reject sys.maxsize directly, so back off if needed.
_limit = sys.maxsize
while True:
    try:
        csv.field_size_limit(_limit)
        break
    except OverflowError:
        _limit = int(_limit / 10)

BASE_DIR = Path(__file__).resolve().parents[2]  # kalomo_project/
RAW_ARTICLES = BASE_DIR / "data" / "raw" / "financial_data" / "raw_scraped_articles.csv"
RAW_PDFS = BASE_DIR / "data" / "raw" / "financial_data" / "raw_scraped_pdfs.csv"
OUT_FILE = BASE_DIR / "data" / "processed" / "db-unza26-csc4792-kalomo_town_council_financial_data.csv"

COUNCIL_NAME = "Kalomo Town Council"


def to_number(amount_str: str) -> float:
    """
    Convert messy amount text into a plain float. Handles:
      'K131,360,483'   -> 131360483.0
      '77, 076, 699'   -> 77076699.0   (PDF text extraction sometimes
                                          inserts stray spaces after commas)
    """
    cleaned = amount_str.replace("K", "").replace(",", "").replace(" ", "").strip()
    return float(cleaned)


def guess_year_from_url(url: str):
    """Pull a plausible fiscal year (2023-2039) out of a filename/URL."""
    match = re.search(r"20(2[3-9]|3[0-9])", url)
    return int(match.group(0)) if match else None


def extract_narrative_records(text: str, source_url: str) -> list:
    """
    Rules for figures written out in prose (news posts, meeting minutes),
    e.g. 'total approved budget of K131,360,483'. Intentionally explicit
    (not 'smart' NLP) so it's easy to explain in your notebook and paper
    exactly why each number was classified the way it was.
    """
    records = []

    # (regex pattern, record_type, fiscal_year, target_or_actual)
    rules = [
        (r"total approved budget of K([\d,]+).{0,40}2026", "total_approved_budget", 2026, "target"),
        (r"2025 approved budget of K([\d,]+)", "total_approved_budget", 2025, "target"),
        (r"OSR\).{0,20}for 2026 is set at K([\d,]+)", "own_source_revenue_budget", 2026, "target"),
        (r"K([\d,]+) allocated in 2025", "own_source_revenue_budget", 2025, "target"),
        (r"Own Source Revenue of K([\d,]+)", "own_source_revenue_budget", 2025, "target"),
        (r"K([\d,]+) from Central Government transfers and cooperating partners",
         "central_govt_transfers_budget", 2025, "target"),
        (r"actual total collections were K([\d,]+)", "total_actual_collections", 2025, "actual"),
        (r"Own Source Revenue collections were K([\d,]+)", "own_source_revenue_actual", 2025, "actual"),
        (r"Central Government transfers and cooperating partner receipts were K([\d,]+)",
         "central_govt_transfers_actual", 2025, "actual"),
        (r"LGEF (?:allocation|disbursement) of K([\d,]+)", "lgef_disbursement", 2026, "actual"),
        (r"CDF (?:allocation|disbursement) of K([\d,]+)", "cdf_disbursement", 2026, "actual"),
        # From the 2025 Budget Consultative Meeting report (community-Engagement-meeting-2025-Budget.pdf):
        # this specific report discusses 2024 calendar-year performance while planning the 2025 budget.
        (r"budget that was approved for 2024 calendar year was K\s?([\d,\s]+?)(?:,? and)",
         "total_approved_budget", 2024, "target"),
        (r"total expenditure for the period under review amounted to K\s?([\d,\s]+?)(?:,? which)",
         "expenditure_actual", 2024, "actual"),
    ]

    for pattern, record_type, year, target_or_actual in rules:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            try:
                amount = to_number(match.group(1))
            except ValueError:
                continue
            records.append({
                "council_name": COUNCIL_NAME,
                "fiscal_year": year,
                "record_type": record_type,
                "amount_zmw": amount,
                "target_or_actual": target_or_actual,
                "source_url": source_url,
            })

    return records


def extract_table_records(text: str, source_url: str) -> list:
    """
    Rules for figures sitting inside budget TABLES, where pdfplumber has
    flattened rows into "label number number number ..." on one line.
    These are more fragile than the narrative rules above -- if the
    council changes their budget document layout, these patterns may
    need updating. Always spot-check a few rows against the source PDF.
    """
    records = []
    year_hint = guess_year_from_url(source_url)

    # --- LGEF: "Local Government Equalisation Fund <approved amount> ..." ---
    # Appears once per annual budget PDF (BUDGET-2026.pdf, 2025-Revised-Budget.pdf).
    m = re.search(r"Local Government\s+Equalisation Fund\s+([\d,]+)", text, re.IGNORECASE)
    if m and year_hint:
        records.append({
            "council_name": COUNCIL_NAME, "fiscal_year": year_hint,
            "record_type": "lgef_disbursement", "amount_zmw": to_number(m.group(1)),
            "target_or_actual": "target", "source_url": source_url,
        })

    # --- Market fees budget line: "Market fees <amount> ..." ---
    m = re.search(r"Market fees\s+([\d,]+)", text, re.IGNORECASE)
    if m and year_hint:
        records.append({
            "council_name": COUNCIL_NAME, "fiscal_year": year_hint,
            "record_type": "market_fees_budget", "amount_zmw": to_number(m.group(1)),
            "target_or_actual": "target", "source_url": source_url,
        })

    # --- Local Taxes: "Local Taxes <approved> <actual> <percent>" ---
    # Found in the 2025 mid-year budget performance report/consultative
    # meeting documents, which review the 2025 approved budget.
    m = re.search(r"Local Taxes\s+([\d,]+)\s+([\d,]+)\s+(\d+)\b", text, re.IGNORECASE)
    if m:
        records.append({
            "council_name": COUNCIL_NAME, "fiscal_year": 2025,
            "record_type": "local_taxes_budget", "amount_zmw": to_number(m.group(1)),
            "target_or_actual": "target", "source_url": source_url,
        })
        records.append({
            "council_name": COUNCIL_NAME, "fiscal_year": 2025,
            "record_type": "local_taxes_actual", "amount_zmw": to_number(m.group(2)),
            "target_or_actual": "actual", "source_url": source_url,
        })

    # --- Fees and Charges: "Fees and Charges <approved> <actual> <percent>" ---
    m = re.search(r"Fees and Charges\s+([\d,]+)\s+([\d,]+)\s+(\d+)\b", text, re.IGNORECASE)
    if m:
        records.append({
            "council_name": COUNCIL_NAME, "fiscal_year": 2025,
            "record_type": "fees_and_charges_budget", "amount_zmw": to_number(m.group(1)),
            "target_or_actual": "target", "source_url": source_url,
        })
        records.append({
            "council_name": COUNCIL_NAME, "fiscal_year": 2025,
            "record_type": "fees_and_charges_actual", "amount_zmw": to_number(m.group(2)),
            "target_or_actual": "actual", "source_url": source_url,
        })

    return records


def extract_records_from_text(text: str, source_url: str, scrape_date: str) -> list:
    # PDF text extraction often breaks sentences across lines in the
    # middle of a phrase (e.g. "total expenditure for\nthe period..."),
    # and a literal space in a regex will NOT match a newline. Collapse
    # all whitespace runs (spaces, tabs, newlines) to a single space
    # before matching so the narrative rules aren't fragile to line
    # wrapping in the source PDFs.
    normalised_text = re.sub(r"\s+", " ", text)
    records = extract_narrative_records(normalised_text, source_url) + extract_table_records(normalised_text, source_url)
    for r in records:
        r["scrape_date"] = scrape_date
    return records


def add_percentages(df: pd.DataFrame) -> pd.DataFrame:
    """Compute percent_of_target where both a target and an actual exist."""
    pairs = {
        "total_actual_collections": "total_approved_budget",
        "own_source_revenue_actual": "own_source_revenue_budget",
        "central_govt_transfers_actual": "central_govt_transfers_budget",
        "expenditure_actual": "total_approved_budget",
        "local_taxes_actual": "local_taxes_budget",
        "fees_and_charges_actual": "fees_and_charges_budget",
    }
    df["percent_of_target"] = None
    for actual_type, target_type in pairs.items():
        actual_rows = df[df["record_type"] == actual_type]
        for idx, row in actual_rows.iterrows():
            target_rows = df[
                (df["record_type"] == target_type) & (df["fiscal_year"] == row["fiscal_year"])
            ]
            if not target_rows.empty:
                target_amount = target_rows.iloc[0]["amount_zmw"]
                if target_amount:
                    df.at[idx, "percent_of_target"] = round(
                        row["amount_zmw"] / target_amount * 100, 1
                    )
    return df


def main():
    all_records = []

    for path in (RAW_ARTICLES, RAW_PDFS):
        if path.exists():
            with open(path, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    all_records.extend(
                        extract_records_from_text(
                            row["raw_text"], row["source_url"], row.get("scrape_date", "")
                        )
                    )

    df = pd.DataFrame(all_records)

    if df.empty:
        print("No records extracted. Check your raw data files -- "
              "have you run the scraping scripts yet?")
        return

    # Drop exact duplicate records (same figure scraped from two places)
    df = df.drop_duplicates(subset=["fiscal_year", "record_type", "amount_zmw"])

    # Add percent_of_target column
    df = add_percentages(df)

    # Add a notes column for anything worth flagging manually
    df["notes"] = ""
    df.loc[df["record_type"] == "own_source_revenue_budget", "notes"] = (
        "OSR budget affected by lower projected plot premium revenue in 2026"
    )
    df.loc[df["record_type"].isin([
        "lgef_disbursement", "market_fees_budget", "local_taxes_budget",
        "local_taxes_actual", "fees_and_charges_budget", "fees_and_charges_actual",
    ]), "notes"] = (
        "Extracted from a flattened PDF budget table; verify against the "
        "source PDF if precision matters, as table layout extraction is "
        "more fragile than prose extraction."
    )

    # Reorder columns to match the data dictionary
    column_order = [
        "council_name", "fiscal_year", "record_type", "amount_zmw",
        "target_or_actual", "source_url", "scrape_date",
        "percent_of_target", "notes",
    ]
    df = df[column_order]

    # Sort for readability
    df = df.sort_values(["fiscal_year", "record_type"]).reset_index(drop=True)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, sep="|", index=False)

    print(f"Saved {len(df)} cleaned records to {OUT_FILE}")
    print(df.to_string())


if __name__ == "__main__":
    main()
