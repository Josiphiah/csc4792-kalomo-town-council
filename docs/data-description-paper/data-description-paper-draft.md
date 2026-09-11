> **STATUS OF THIS DRAFT (remove before final submission):** Sections marked
> **[TODO — blocked]** depend on the CDF, financial, and administrative/
> governance datasets (Louis, Faiz, Nicholas), which had not been scraped
> yet as of this draft. Everything else below is complete. Once those three
> CSVs exist, update the marked sections with their real row counts and
> final column names, then paste this content into the official Elsevier
> Data in Brief Word/LaTeX template downloaded from
> https://www.elsevier.com/dib-template (a JS-rendered page; the template
> file itself must be downloaded manually via a browser — it could not be
> fetched automatically) and re-check formatting against the guide for
> authors: https://www.sciencedirect.com/journal/data-in-brief/publish/guide-for-authors

# Title

A Dataset of Constituency Development Fund (CDF) Projects, Council Finances, Governance Structures, and Development Plans for Kalomo Town Council, Zambia

# Authors and affiliations

Louis, Faiz, Nicholas, Goodson, Josiphiah Simbaya

Department of Computing and Informatics, University of Zambia, Lusaka, Zambia

*(CSC 4792: Data Mining and Warehousing — Group Mini Project, 2026)*

# Abstract

*(~150 words)*

This dataset compiles publicly available records from Kalomo Town Council, Southern Province, Zambia, covering four dimensions of local governance: Constituency Development Fund (CDF) projects and allocations, council budgets and locally generated revenue, administrative and governance structures (leadership, wards, Ward Development Committees), and development/strategic plans (including the council's Integrated Development Plan 2021–2030). Zambia's decentralisation agenda, formalised through the Local Government Act No. 2 of 2019 and the 2023 National Decentralisation Policy, devolves significant planning and financial responsibility to local authorities such as Kalomo Town Council, yet council-level data of this kind is rarely available in structured form. The dataset was built by systematically scraping the council's official website and downloadable PDF publications with Python (`requests`, `BeautifulSoup`, `pdfplumber`), then manually structuring and cleaning the extracted content into four pipe-separated CSV files. It is intended to support research on decentralised local governance, CDF utilisation, and local-authority planning in Zambia.

# Specifications Table

| Subject | Description |
|---|---|
| Subject | Public administration; local government; decentralisation (Zambia) |
| Specific subject area | Constituency Development Fund (CDF) projects, council finances/revenue, governance and administrative structures, and development/strategic plans for a single Zambian town council |
| Type of data | Tables (CSV) |
| Data format | Raw (scraped PDFs/HTML, not distributed) and processed/filtered (final CSVs, pipe `\|`-separated, UTF-8) |
| How data were acquired | Web scraping and PDF text extraction using Python (`requests` for HTTP, `BeautifulSoup` for HTML parsing, `pdfplumber` for PDF text extraction), followed by manual structuring of unstructured/prose source documents into tabular rows |
| Data source location | Kalomo Town Council, Southern Province, Zambia (institution: Kalomo Town Council; primary source: https://www.kalomocouncil.gov.zm) |
| Data accessibility | Repository: GitHub — https://github.com/Josiphiah/csc4792-kalomo-town-council<br>Kaggle dataset: **[TODO — blocked: link once Goodson publishes the Kaggle dataset]** |
| Related research article | None |

# Value of the Data

- Provides one of the few structured, machine-readable datasets on Constituency Development Fund (CDF) allocation and project delivery at the individual-council level in Zambia, useful to researchers studying fiscal decentralisation and local development financing.
- Documents Kalomo Town Council's actual Integrated Development Plan (2021–2030) targets alongside real 2025 procurement activity, allowing comparison between what was *planned* and what is *currently being implemented*.
- Useful to journalists and civil-society organisations monitoring public fund utilisation and project delivery at the constituency level.
- Provides a template/methodology (web scraping + manual structuring of prose government PDFs) that other researchers or students could replicate for other Zambian local authorities, most of which publish similarly unstructured records.
- Supports teaching and coursework in data mining, web scraping, and public-sector data curation, as it was itself produced for that purpose.

# Data Description

## `db-unza26-csc4792-kalomo_town_council_development_plans.csv`

20 rows, 9 columns, pipe (`\|`)-separated. Each row is either a distinct planning/policy document published by or applicable to Kalomo Town Council, or an individual project listed in the council's own Integrated Development Plan (IDP) Capital Investment Plan.

| Column | Type | Description |
|---|---|---|
| `record_id` | string | Unique identifier, `DP-001`–`DP-020` |
| `plan_name` | string | Name of the plan, policy, or project |
| `plan_type` | string | e.g. IDP, Policy, Strategy, ESMP, Capital Investment Project |
| `sector` | string | Sector the plan/project belongs to (e.g. Health, Water & Sanitation, Governance) |
| `period` | string | Plan period where stated (e.g. `2021-2030`), else `N/A` |
| `description` | string | Summary of the plan/project, including any known extraction limitations |
| `status` | string | Current status (e.g. Adopted, Planned, Ongoing, In force) |
| `source_url` | string | Direct URL to the source PDF on the council's website |
| `date_scraped` | date (YYYY-MM-DD) | Date the record was collected |

Notable content: the actual Kalomo District Integrated Development Plan (2021–2030), the council's Investment Profile 2.0, the National Decentralisation Policy (2023), the 2025 Procurement Plan, and the ten named projects in the IDP's own Capital Investment Plan table (e.g. "Construction of a Truck Yard", "Construction of Health Facilities") — the source table itself does not publish budgeted amounts for these projects, which is recorded honestly in the `status` field rather than estimated.

## `db-unza26-csc4792-kalomo_town_council_cdf_projects.csv`

**[TODO — blocked, owner: Louis]** Planned columns (per `docs/DATA_DICTIONARY.md`): `project_id`, `project_name`, `ward`, `sector`, `amount_allocated_zmw`, `amount_disbursed_zmw`, `fiscal_year`, `status`, `source_url`, `date_scraped`. Update this subsection with final row count and any column changes once scraping/cleaning is complete.

## `db-unza26-csc4792-kalomo_town_council_financial_data.csv`

**[TODO — blocked, owner: Faiz]** Planned columns (per `docs/DATA_DICTIONARY.md`): `record_id`, `fiscal_year`, `category`, `description`, `amount_zmw`, `source_url`, `date_scraped`. Update this subsection with final row count and any column changes once scraping/cleaning is complete.

## `db-unza26-csc4792-kalomo_town_council_administrative_governance.csv`

**[TODO — blocked, owner: Nicholas]** Planned columns (per `docs/DATA_DICTIONARY.md`): `record_id`, `record_type`, `name_or_title`, `role_or_function`, `ward`, `date`, `source_url`, `date_scraped`. Update this subsection with final row count and any column changes once scraping/cleaning is complete.

# Experimental Design, Materials and Methods

## Overall approach

All four datasets were built using the same three-stage process:

1. **Manual exploration.** Each dataset owner first browsed the council's website (https://www.kalomocouncil.gov.zm) by hand to identify which pages and downloadable PDFs were relevant to their assigned topic, since the site's navigation structure does not map cleanly onto the four dataset categories (for example, planning documents relevant to the development-plans dataset are split across a "ZDSP" page and hidden tabs on a "Publications" page, discovered only by inspecting the page's underlying HTML).
2. **Automated scraping.** A Python script per dataset (`scripts/scraping/scrape_*.py`) used `requests` and `BeautifulSoup` to fetch the identified pages, extract links to relevant PDFs, download them, and — where the source is a text-based PDF — extract their text with `pdfplumber` for review.
3. **Manual structuring and cleaning.** Because the council's source documents are prose reports and policy PDFs rather than structured data tables, each extracted document was read manually and the relevant facts (project names, amounts, dates, statuses, sectors) were transcribed into row dictionaries in a corresponding `scripts/cleaning/clean_*.py` script, which also applies the project-wide standardisation rules below before writing the final CSV.

## Standardisation rules applied to every dataset

- Filenames follow `db-unza26-csc4792-kalomo_town_council_[description].csv`, all lowercase, underscore-separated.
- All processed CSVs use the pipe character (`\|`) as the column separator, not a comma.
- Every row carries a `source_url` column pointing to the exact page or PDF it was drawn from, and a `date_scraped` column.
- Missing values are written as the literal string `N/A` throughout — never a mix of blank cells, dashes, or the word "unknown".
- Duplicate rows are dropped on a dataset-appropriate key before the final CSV is written.

## Legal and policy context

Zambia's local authorities, including Kalomo Town Council, operate under the **Local Government Act No. 2 of 2019** and its subsequent amendments, which establish councils' planning and financial-management mandates. The **Constituency Development Fund Act No. 11 of 2018** governs CDF allocation and utilisation at constituency level (Kalomo Central and Dundumwezi constituencies, in Kalomo's case). The **National Decentralisation Policy** (Office of the President, Cabinet Office, revised March 2023, themed *"Realising Local Development through Citizen Participation"*) sets the current national policy framework for devolved local governance, superseding the 2013 policy, and is the direct basis for the Local Government Equalisation Fund (LGEF) and the Zambia Devolution Support Programme (ZDSP) referenced throughout this dataset. This legal and policy context is the reason CDF, LGEF, and IDP-related fields were prioritised as the core structure of this dataset rather than an arbitrary schema.

## Tools used

Python 3, `requests`, `beautifulsoup4`, `lxml`, `pandas`, `pdfplumber`, `python-dateutil`, Jupyter Notebook.

# Ethics and limitations

All data in this dataset was collected exclusively from publicly available, unauthenticated pages and downloadable publications on Kalomo Town Council's official website. No personal, private, or restricted data was collected; no login, payment, or access credential was used or bypassed at any point.

Known limitations, documented rather than concealed:

- The council's website serves an incomplete TLS certificate chain; scraping required disabling certificate verification for this specific host. No credentials are transmitted by any request in this project, so this affects only tamper-detection on public GET requests, not data confidentiality.
- Four of the ten PDFs relevant to the development-plans dataset are scanned images with no meaningful extractable text layer; no OCR step was applied given the project timeline, so those four records carry less descriptive detail than the others, and this is stated explicitly in their `description` field rather than inferred.
- The IDP's own published Capital Investment Plan table (Table 28) does not list budgeted amounts for its ten proposed projects — this is a gap in the source document itself, not a data-collection failure, and is recorded as such rather than estimated.
- **[TODO — blocked]** Note any equivalent limitations Louis, Faiz, and Nicholas encounter in their datasets (e.g. whether a standalone budget/IDP document was or wasn't publicly available for the financial dataset, per the project's fallback guidance).

# CRediT author statement

**[TODO — confirm final wording with each teammate before submission]**

- **Louis:** Scraping and cleaning — CDF and community-project data.
- **Faiz:** Scraping and cleaning — financial and revenue data.
- **Nicholas:** Scraping and cleaning — administrative and governance data.
- **Josiphiah Simbaya:** Scraping and cleaning — development plans data; Writing – original draft (Data in Brief paper); notebook documentation for the development-plans dataset.
- **Goodson:** Project coordination and repository setup; data dictionary; data integration and validation; Kaggle dataset publication.

# References

1. Republic of Zambia. *The Local Government Act No. 2 of 2019.* Lusaka: Government Printer; 2019.
2. Republic of Zambia. *The Constituency Development Fund Act No. 11 of 2018.* Lusaka: Government Printer; 2018.
3. Office of the President, Cabinet Office, Republic of Zambia. *The National Decentralisation Policy — "Realising Local Development through Citizen Participation".* Lusaka; 2023.
4. Ministry of Local Government and Rural Development, Republic of Zambia. Available from: https://www.mlgrd.gov.zm
5. Kalomo Town Council. *Kalomo District Integrated Development Plan (2021–2030).* Kalomo Town Council; 2023.
6. Phiri, L. **[TODO — copy the exact citation for the exemplar dataset from the assignment brief's own bibliography; not reproduced here as the brief text was not available while drafting this section]**

> **[TODO]** Confirm whether the brief's bibliography also cites specific amendment Acts to the Local Government Act (referenced in the project plan as "2023 and 2026 amendments") — no such amendment Act was found or verified during scraping (only the 2019 Act itself was found listed on the council's Publications page), so none is cited here without verification.
