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
| record_id | string | Unique identifier assigned during cleaning |
| fiscal_year | string | Financial year the record applies to |
| category | string | e.g. Approved Budget, LGEF Utilisation, Market Fees, Local Tax, Levy |
| description | string | Free-text description of the revenue/expenditure line |
| amount_zmw | float | Amount in Zambian Kwacha |
| source_url | string | URL of the page the record was scraped from |
| date_scraped | date (YYYY-MM-DD) | Date the record was collected |

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
