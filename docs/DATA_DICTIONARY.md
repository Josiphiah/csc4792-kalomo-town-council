# Data Dictionary

Documents every column in each processed (Kaggle-ready) CSV under `data/processed/`.
All files are pipe (`|`) separated. Update this file whenever a column is added,
renamed, or its meaning changes.

## db-unza26-csc4792-kalomo_town_council_cdf_projects.csv

| Column | Type | Description |
|---|---|---|
| project_id | string | Unique identifier assigned during cleaning |
| project_name | string | Name/title of the CDF project |
| ward | string | Ward in which the project is located |
| sector | string | e.g. Education, Health, Water & Sanitation, Roads |
| amount_allocated_zmw | float | CDF amount allocated to the project (ZMW) |
| amount_disbursed_zmw | float | CDF amount disbursed to date (ZMW) |
| fiscal_year | string | Financial year the allocation applies to |
| status | string | e.g. Planned, Ongoing, Completed, Stalled |
| source_url | string | URL of the page the record was scraped from |
| date_scraped | date (YYYY-MM-DD) | Date the record was collected |

## db-unza26-csc4792-kalomo_town_council_financial_data.csv

| Column | Type | Description |
|---|---|---|
| council_name | string | Name of the council (always "Kalomo Town Council" in this file) |
| fiscal_year | integer | The financial year the figure relates to (e.g. 2025, 2026) |
| record_type | string | What kind of figure this is. See "Record type definitions" below |
| amount_zmw | float | The monetary amount in Zambian Kwacha (ZMW), with currency symbols and commas removed |
| target_or_actual | string | Whether the figure is a "target" (budgeted/projected) or "actual" (collected/received/disbursed) |
| source_url | string | The exact page or document the figure was extracted from, for provenance and verification |
| date_scraped | date (YYYY-MM-DD) | The date the source page/document was scraped, for provenance and reproducibility |
| percent_of_target | float | For "actual" rows only: what percentage of the matching target was achieved. Blank for targets |
| notes | string | Free-text context on the figure, where relevant (e.g. reasons for a revenue drop) |

### Record type definitions
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

## db-unza26-csc4792-kalomo_town_council_administrative_governance.csv

| Column | Type | Description |
|---|---|---|
| record_id | string | Unique identifier assigned during cleaning |
| record_type | string | Contact, Leadership, Department, Ward, Committee (WDC/CWAC/SDMC/Headmen/CDFC), Constituency, Chiefdom, Service, Resolution, Report |
| name_or_title | string | Name of official/department/ward/committee/constituency/chiefdom/resolution/report |
| role_or_function | string | Role/mandate/function, including any sourcing caveats (e.g. leadership transitions, national vs. Council office) |
| ward | string | Associated ward, where applicable ("All 20 wards" for district-wide committees, N/A otherwise) |
| date | date (YYYY-MM-DD) | Date of appointment/resolution/notice; N/A where the source did not state one - see source_pages_extract.txt for why |
| source_url | string | URL of the page the record was scraped from, OR a document title/date citation for uploaded scanned sources with no public URL (clearly labelled "uploaded scan, no public URL") |
| date_scraped | date (YYYY-MM-DD) | Date the record was collected |

> Coverage note: the ward councillor roster is complete (20/20 wards), and
> the department directory is complete for everything under the Office of
> the Council Secretary (5 units) plus 3 line departments. As of
> 2026-09-12, three uploaded scanned meeting-minutes documents (Dundumwezi
> CDF Committee, Kalomo Central CDF Committee, and a Community Engagement
> Budget Preparation meeting) closed the previously-open "meeting
> resolutions, public notices, and reports" gap - see
> `data/raw/administrative_governance/source_pages_extract.txt` for full
> sourcing, including named WDC Chairpersons for 14 of 20 wards. Detailed
> CDF project-level figures and financial performance tables within those
> same documents were deliberately NOT duplicated here - that level of
> detail belongs in the team's separate cdf_projects and financial_data
> datasets, and is flagged as such in the source notes for whoever owns
> those files.

## db-unza26-csc4792-kalomo_town_council_development_plans.csv

| Column | Type | Description |
|---|---|---|
| record_id | string | Unique identifier assigned during cleaning |
| plan_name | string | Name of the IDP/strategic plan/sector project |
| plan_type | string | e.g. IDP, Strategic Plan, Sector Project |
| sector | string | Sector the plan/project belongs to |
| period | string | Plan period, e.g. 2022-2026 |
| description | string | Summary of the plan/project |
| status | string | Current status, where available |
| source_url | string | URL of the page the record was scraped from |
| date_scraped | date (YYYY-MM-DD) | Date the record was collected |

> Note: column sets above are a starting template. Each data owner should
> confirm final columns against what is actually scrapable from the council's
> site and update this file + the corresponding CSV header together.
