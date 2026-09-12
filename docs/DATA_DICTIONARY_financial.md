# Data Dictionary — Financial & Revenue Dataset

File: `data/processed/db-unza26-csc4792-kalomo_town_council_financial_data.csv`
Separator: `|` (pipe)

| Column              | Type    | Description                                                                                     |
|---------------------|---------|-----------------------------------------------------------------------------------------------------|
| council_name        | string  | Name of the council (always "Kalomo Town Council" in this file).                                    |
| fiscal_year         | integer | The financial year the figure relates to (e.g. 2025, 2026).                                         |
| record_type         | string  | What kind of figure this is. See "Record type definitions" below.                                   |
| amount_zmw          | float   | The monetary amount in Zambian Kwacha (ZMW), with currency symbols and commas removed.               |
| target_or_actual    | string  | Whether the figure is a "target" (budgeted/projected) or "actual" (collected/received/disbursed).    |
| source_url          | string  | The exact page or document the figure was extracted from, for provenance and verification.           |
| scrape_date         | date    | The date (YYYY-MM-DD) the source page/document was scraped, for provenance and reproducibility.      |
| percent_of_target   | float   | For "actual" rows only: what percentage of the matching target was achieved. Blank for targets.      |
| notes               | string  | Free-text context on the figure, where relevant (e.g. reasons for a revenue drop).                   |

## Record type definitions
- **total_approved_budget** — the council's overall approved budget for the year.
- **own_source_revenue_budget** — targeted revenue the council expects to raise itself (market fees, levies, plot premiums, local taxes, etc.), before collection.
- **central_govt_transfers_budget** — targeted funding expected from central government and cooperating partners.
- **total_actual_collections** — actual total revenue collected against the total approved budget.
- **own_source_revenue_actual** — actual Own Source Revenue collected.
- **central_govt_transfers_actual** — actual Central Government transfer/cooperating partner receipts.
- **lgef_disbursement** — Local Government Equalisation Fund amount budgeted/disbursed.
- **cdf_disbursement** — Constituency Development Fund amount disbursed/received.
- **market_fees_budget** — budgeted revenue from council market fees.
- **local_taxes_budget** / **local_taxes_actual** — budgeted vs. actual revenue from local taxes/rates.
- **fees_and_charges_budget** / **fees_and_charges_actual** — budgeted vs. actual revenue from council fees and charges.
- **expenditure_actual** — actual total expenditure reported for a given fiscal year (e.g. the 2024 figure came from a mid-year review document reporting on 2024 spending). Compared against that year's `total_approved_budget` to calculate `percent_of_target`.

> Rows with `record_type` values ending in `_budget` came from flattened
> PDF budget tables (pdfplumber reads tables as plain lines of text,
> without column boundaries). These are more fragile than the
> prose-based rows above — always spot-check a few against the source
> PDF listed in `source_url`, and note this limitation in your Data in
> Brief paper's methodology section.
>
> If your scraped data surfaces a figure that doesn't fit one of the
> above, add a new `record_type` value here describing it, rather than
> forcing it into an existing category.
