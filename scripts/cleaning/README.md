# Cleaning / preprocessing scripts

One script per dataset that takes the corresponding `data/raw/<dataset>/`
files and produces the final pipe-separated CSV in `data/processed/`,
following the naming convention `db-unza26-csc4792-[description].csv` and the
columns defined in `docs/DATA_DICTIONARY.md`.

| Script (planned) | Owner | Output |
|---|---|---|
| `clean_cdf_projects.py` | Louis | `data/processed/db-unza26-csc4792-kalomo_town_council_cdf_projects.csv` |
| `clean_financial_data.py` | Faiz | `data/processed/db-unza26-csc4792-kalomo_town_council_financial_data.csv` |
| `clean_administrative_governance.py` | Nicholas | `data/processed/db-unza26-csc4792-kalomo_town_council_administrative_governance.csv` |
| `clean_development_plans.py` | Josiphiah | `data/processed/db-unza26-csc4792-kalomo_town_council_development_plans.csv` |
