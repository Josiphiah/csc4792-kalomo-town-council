"""
Build the final development-plans dataset from the documents downloaded by
scrape_development_plans.py.

Most of the source documents here are prose planning/policy PDFs, not
tables, so (as with the CDF dataset) each row below was produced by reading
the extracted text in data/raw/development_plans/*_extract.txt and manually
pulling out the plan/project name, sector, period and status - the same
approach the project brief recommends for unstructured council documents.

Two categories of row are included:

  1. Document-level rows - one row per distinct planning/policy document
     found on the council site (the IDP itself, the Investment Profile,
     the National Decentralisation Policy, etc).
  2. Project-level rows - the ten individual projects listed in the IDP's
     own "Table 28: Capital Investment Plan" (2021 - 2030), so the dataset
     captures actual proposed projects and not just document titles.

Four of the fourteen downloaded PDFs are scanned/rotated image files with
no extractable text layer (confirmed: pdfplumber returns 0 characters even
though the file downloads fine). Those are still included as rows - status
and description note the extraction limitation - rather than silently
dropped, per the brief's instruction to document gaps honestly instead of
fabricating detail we can't verify.
"""

import os
from datetime import date

import pandas as pd

OUT_PATH = os.path.join(
    "data", "processed", "db-unza26-csc4792-kalomo_town_council_development_plans.csv"
)

SCRAPE_DATE = date.today().isoformat()

IDP_URL = "https://www.kalomocouncil.gov.zm/wp-content/uploads/2025/12/KALOMO-IDP-FINAL-JANUARY-2023-LAUNCH-1-1-2.pdf"

# --- 1. Document-level rows -------------------------------------------------
DOCUMENTS = [
    dict(
        plan_name="Kalomo District Integrated Development Plan (IDP) 2021-2030",
        plan_type="IDP",
        sector="Multi-sector",
        period="2021-2030",
        description=(
            "District-wide Integrated Development Plan prepared under the Urban and "
            "Regional Planning Act No. 3 of 2015, covering social, economic, "
            "environmental, spatial, infrastructural, institutional and governance "
            "development across Kalomo district's 20 wards. Vision: 'A climate "
            "resilient district that is economically prosperous, and anchored on "
            "sustainable use of local resources.'"
        ),
        status="Adopted",
        source_url=IDP_URL,
    ),
    dict(
        plan_name="Kalomo Town Council 2.0 Investment Profile",
        plan_type="Investment Profile",
        sector="Investment/Economic Development",
        period="N/A",
        description=(
            "Investor-facing profile covering potential viable economic sectors "
            "(agriculture and dairy/milk processing, tourism, natural resource "
            "management, small-scale enterprises), infrastructure availability, "
            "and investment requirements/profitability analysis for the district."
        ),
        status="Published",
        source_url="https://www.kalomocouncil.gov.zm/wp-content/uploads/2025/11/Kalomo-town-Council-2.0-Investment-Profile-1-1.pdf",
    ),
    dict(
        plan_name="National Decentralisation Policy (2023)",
        plan_type="Policy",
        sector="Governance/Decentralisation",
        period="2023",
        description=(
            "Revised national policy (Office of the President, Cabinet Office, "
            "March 2023) themed 'Realising Local Development through Citizen "
            "Participation', superseding the 2013 policy. Sets the legal/policy "
            "basis for CDF, LGEF and devolved local-governance functions "
            "referenced across the other datasets in this project."
        ),
        status="In force",
        source_url="https://www.kalomocouncil.gov.zm/wp-content/uploads/2025/11/National-Decentralisation-Policy-2023.pdf",
    ),
    dict(
        plan_name="Council Citizen Engagement Strategy (Output-Based Budgeting focus)",
        plan_type="Strategy",
        sector="Governance/Public Participation",
        period="2025",
        description=(
            "Ministry of Local Government and Rural Development / Zambia "
            "Devolution Support Programme (ZDSP) template strategy for "
            "structuring citizen engagement, communication, budgeting and "
            "monitoring of council project implementation."
        ),
        status="Draft/template (marked 'Official Use Only' in source)",
        source_url="https://www.kalomocouncil.gov.zm/wp-content/uploads/2025/11/Citizen_Engagement_Strategy.pdf",
    ),
    dict(
        plan_name="Stakeholders Engagement Plan 2025",
        plan_type="Plan",
        sector="Governance/Public Participation",
        period="2025",
        description=(
            "Council's 2025 stakeholder engagement plan. Source PDF is a "
            "scanned image file with no extractable text layer, so content is "
            "documented from its listing under the council's Publications > "
            "Engagement Plan tab rather than full text."
        ),
        status="Published",
        source_url="https://www.kalomocouncil.gov.zm/wp-content/uploads/2025/12/2025-STAKEHOLDER-ENGAGEMENT-PLAN.pdf",
    ),
    dict(
        plan_name="Kalomo Town Council Procurement Plan 2025",
        plan_type="Plan",
        sector="Procurement",
        period="2025",
        description=(
            "Annual procurement plan (version 1, last updated 22 July 2025) "
            "listing planned works/goods/services contracts, e.g. Truck Yard "
            "wall fence completion, Tandabale Market Shelter completion, dump "
            "truck purchase, staff house construction. Total procurement "
            "budget ZMW 47,993,371.87."
        ),
        status="Active",
        source_url="https://www.kalomocouncil.gov.zm/wp-content/uploads/2025/08/plan.pdf",
    ),
    dict(
        plan_name="The Local Authorities Debt and Arrears Monitoring Mechanism",
        plan_type="Mechanism/Policy",
        sector="Finance",
        period="2023",
        description=(
            "National-level (Republic of Zambia) mechanism, published December "
            "2023, for tracking and managing debt/arrears across local "
            "authorities; referenced by Kalomo Town Council as a guiding "
            "financial-management document."
        ),
        status="In force",
        source_url="https://www.kalomocouncil.gov.zm/wp-content/uploads/2025/11/Debt-Arrears-Monitoring-Mechanism-FINAL-COPY8-min.pdf",
    ),
    dict(
        plan_name="ZDSP Proposed Projects list",
        plan_type="Project List (ZDSP)",
        sector="Multi-sector",
        period="N/A",
        description=(
            "Council-submitted list of proposed projects under the Zambia "
            "Devolution Support Programme (ZDSP). Source PDF is a scanned, "
            "rotated image file with no extractable text layer, so content is "
            "documented from its listing on the council's ZDSP Projects page "
            "rather than full text."
        ),
        status="Proposed",
        source_url="https://www.kalomocouncil.gov.zm/wp-content/uploads/2025/11/ZDSP-PROPOSED-PROJECTS_rotated.pdf",
    ),
    dict(
        plan_name="Truck Parking Bay - Environmental and Social Management Plan",
        plan_type="ESMP",
        sector="Infrastructure/Transport",
        period="N/A",
        description=(
            "Project-level environmental and social safeguard plan for the "
            "proposed Truck Parking Bay development. Source PDF is a scanned "
            "image file with no extractable text layer."
        ),
        status="Planned",
        source_url="https://www.kalomocouncil.gov.zm/wp-content/uploads/2025/06/ESMP-TRUCK-PARKING-BAY.pdf",
    ),
    dict(
        plan_name="Tandabale Market Shelter - Environmental and Social Management Plan",
        plan_type="ESMP",
        sector="Infrastructure/Markets",
        period="N/A",
        description=(
            "Project-level environmental and social safeguard plan for the "
            "Tandabale Market Shelter. Cross-referenced in the 2025 "
            "Procurement Plan as an active works contract ('Completion of a "
            "Market Shelter at Tandabale Market', ref KTC/2025/6). Source PDF "
            "is a scanned image file with no extractable text layer."
        ),
        status="Ongoing (per 2025 Procurement Plan)",
        source_url="https://www.kalomocouncil.gov.zm/wp-content/uploads/2025/06/ESMP-TANDABALE-MARKET-SHELTER.pdf",
    ),
]

# --- 2. IDP Table 28 "Capital Investment Plan" project-level rows ----------
# Verified with pdfplumber's extract_tables() directly on IDP page 152: the
# "Amount (ZMW)" and "S/N" columns are genuinely blank in the source PDF,
# not a table-extraction failure - the council published this table without
# filling in budgeted amounts. We record that honestly (status note) rather
# than inventing figures.
CAPITAL_INVESTMENT_PROJECTS = [
    ("Construction of a Truck Yard", "Transport/Infrastructure",
     "Ongoing - cross-referenced as 'Completion of a Truck Yard wall fence' (KTC/2025/2) in the 2025 Procurement Plan"),
    ("Construction of Dams", "Water & Sanitation",
     "Planned (amount not specified in source IDP)"),
    ("Construction of Roads", "Roads/Transport",
     "Planned (amount not specified in source IDP)"),
    ("Construction of Schools", "Education",
     "Planned (amount not specified in source IDP)"),
    ("Construction of Staff Houses", "Housing/Administration",
     "Planned (amount not specified in source IDP)"),
    ("Construction of Dip Tanks", "Agriculture/Livestock",
     "Planned (amount not specified in source IDP)"),
    ("Construction of Health Facilities", "Health",
     "Planned (amount not specified in source IDP)"),
    ("Construction of Manufacturing and Processing Factories (Industrialisation)", "Industry/Economic Development",
     "Planned (amount not specified in source IDP)"),
    ("Construction of Play Parks (Recreation Facilities)", "Recreation/Social Services",
     "Planned (amount not specified in source IDP)"),
    ("Construction of Storage Shades", "Commerce & Trade",
     "Planned (amount not specified in source IDP)"),
]


def build_rows():
    rows = list(DOCUMENTS)
    for name, sector, status in CAPITAL_INVESTMENT_PROJECTS:
        rows.append(dict(
            plan_name=name,
            plan_type="Capital Investment Project (IDP Table 28)",
            sector=sector,
            period="2021-2030",
            description=(
                f"Project listed in the IDP's Capital Investment Plan (Table 28, "
                f"page 152 of the document)."
            ),
            status=status,
            source_url=IDP_URL,
        ))
    return rows


def main():
    rows = build_rows()
    df = pd.DataFrame(rows)

    # --- standardisation, matching the project-wide cleaning conventions ---
    df["record_id"] = [f"DP-{i+1:03d}" for i in range(len(df))]
    df = df[["record_id", "plan_name", "plan_type", "sector", "period",
             "description", "status", "source_url"]]

    df["date_scraped"] = SCRAPE_DATE

    for col in ["plan_name", "plan_type", "sector", "period", "description", "status"]:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"": "N/A", "nan": "N/A", "None": "N/A"})

    df = df.drop_duplicates(subset=["plan_name", "source_url"]).reset_index(drop=True)

    assert df["source_url"].str.startswith("https://").all(), "every row must have a working https source_url"
    assert not df["record_id"].duplicated().any(), "record_id must be unique"

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, sep="|", index=False)
    print(f"Wrote {len(df)} rows to {OUT_PATH}")
    print(df[["record_id", "plan_name", "plan_type", "status"]].to_string(index=False))


if __name__ == "__main__":
    main()
