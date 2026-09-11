# Scraping scripts

One script per dataset, targeting https://www.kalomocouncil.gov.zm/. Each
script should write its raw output to the matching `data/raw/<dataset>/`
folder (JSON or HTML snapshots are fine at this stage — cleaning happens
separately in `scripts/cleaning/`).

| Script (planned) | Owner | Output |
|---|---|---|
| `scrape_cdf_projects.py` | Louis | `data/raw/cdf_projects/` |
| `scrape_financial_data.py` | Faiz | `data/raw/financial_data/` |
| `scrape_administrative_governance.py` | Nicholas | `data/raw/administrative_governance/` |
| `scrape_development_plans.py` | Josiphiah | `data/raw/development_plans/` |
