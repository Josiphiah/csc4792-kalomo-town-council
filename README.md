# CSC4792 Mini Project — Kalomo Town Council Dataset

A curated dataset on the Constituency Development Fund (CDF), council finances,
administrative/governance structures, and development plans of **Kalomo Town
Council**, Zambia — built for the CSC4792 group mini-project (University of
Zambia, 2026).

## Team

| Member | Role | Output |
|---|---|---|
| Goodson (coordinator) | Project coordination and data integration | Repo structure, data dictionary, master CSVs, naming/format checks, Kaggle upload |
| Louis | CDF and community-project data collection | `db-unza26-csc4792-kalomo_town_council_cdf_projects.csv` |
| Faiz | Financial and revenue data collection | `db-unza26-csc4792-kalomo_town_council_financial_data.csv` |
| Nicholas | Council administration and governance data | `db-unza26-csc4792-kalomo_town_council_administrative_governance.csv` |
| Josiphiah | Development plans, documentation, notebook support | IDP/strategic plan data, Data in Brief paper, notebook markdown documentation |

## Source

Data is scraped from Kalomo Town Council's official website,
[kalomocouncil.gov.zm](https://www.kalomocouncil.gov.zm/), as catalogued by
the Ministry of Local Government and Rural Development
(https://www.mlgrd.gov.zm), supplemented by publicly available council
notices, budget speeches, and CDF disbursement reports.

## Repository structure

```
data/
  raw/                          # unprocessed scraped data, one subfolder per dataset
    cdf_projects/
    financial_data/
    administrative_governance/
    development_plans/
  processed/                    # final, cleaned, pipe-separated CSVs (Kaggle-ready)
notebooks/                      # Jupyter notebook(s) documenting scraping + cleaning
scripts/
  scraping/                     # web scraping scripts, one per dataset
  cleaning/                     # data cleaning / preprocessing scripts
docs/
  data-description-paper/       # Data in Brief manuscript + submission PDF
  DATA_DICTIONARY.md            # column-level documentation for every processed CSV
```

## Dataset naming convention

All processed CSV files use the pipe character `|` as the column separator and
follow the naming convention:

```
db-unza26-csc4792-[description].csv
```

e.g. `db-unza26-csc4792-kalomo_town_council_cdf_projects.csv`

## Kaggle dataset

Link: https://www.kaggle.com/datasets/goodsonmwensojr/kalomo-town-council-dataset

## License / attribution

Built by Group [44], CSC4792, University of Zambia, 2026. Data sourced from
public council records; see the Data in Brief paper for full methodology and
provenance.
