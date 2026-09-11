"""
Build the final administrative/governance dataset for Kalomo Town Council.

As with the development-plans dataset, this council's governance
information is spread across prose pages and news posts rather than
tables, so each row below was compiled by reading
data/raw/administrative_governance/source_pages_extract.txt (itself built
from scrape_administrative_governance.py's target pages) and pulling out
the name/title, role, ward and date for each governance record - the same
manual-extraction approach used for the unstructured council documents in
clean_development_plans.py.

Row categories:
  1. Leadership       - council/political/traditional office holders
  2. Department        - confirmed council departments/offices
  3. Ward / Councillor - elected ward-level representatives
  4. Committee          - grassroots governance bodies (WDC, CWAC, SDMC)
  5. Constituency        - the district's two parliamentary constituencies
  6. Chiefdom              - the district's three traditional chiefdoms

Where a detail (an exact appointment date, a full committee roster) was
not confirmable from the available sources, that gap is recorded in the
row rather than invented - consistent with the rest of this project.
"""

import os
from datetime import date

import pandas as pd

OUT_PATH = os.path.join(
    "data", "processed",
    "db-unza26-csc4792-kalomo_town_council_administrative_governance.csv",
)

SCRAPE_DATE = date.today().isoformat()

CIVIC_LEADERS_URL = "https://www.kalomocouncil.gov.zm/?page_id=2871"
ABOUT_URL = "https://www.kalomocouncil.gov.zm/?page_id=118"
PROFILE_URL = "https://www.kalomocouncil.gov.zm/?page_id=2242"
FAQS_URL = "https://www.kalomocouncil.gov.zm/?page_id=2259"
CDF_EVENT_URL = "https://www.kalomocouncil.gov.zm/?p=1799"
BUDGET_MEETING_URL = "https://www.kalomocouncil.gov.zm/?p=3782"
MIS_LAUNCH_URL = "https://www.kalomocouncil.gov.zm/?p=4672"
RCFW_URL = "https://www.kalomocouncil.gov.zm/?p=5104"
WIKIPEDIA_KALOMO_CENTRAL = "https://en.wikipedia.org/wiki/Kalomo_Central"
WIKIPEDIA_DUNDUMWENZI = "https://en.wikipedia.org/wiki/Dundumwenzi_(constituency)"

FOOTER_URL = "https://www.kalomocouncil.gov.zm/?page_id=770"  # captured from the site-wide footer

RECORDS = [
    # --- 0. Contact ------------------------------------------------------
    dict(
        record_type="Contact",
        name_or_title="Kalomo Town Council - General Contact Information",
        role_or_function=(
            "Email: towncouncilkalomo@gmail.com | Address: 128 Independence "
            "Avenue, along T1 Livingstone-Lusaka road, Southern Province, "
            "Zambia | P.O. Box 620062 | Office hours: Mon-Fri 08:00-17:00 Hrs"
        ),
        ward="N/A",
        date="N/A",
        source_url=FOOTER_URL,
    ),

    # --- 1. Leadership -------------------------------------------------
    dict(
        record_type="Leadership",
        name_or_title="Coy Makaya",
        role_or_function="Council Chairperson",
        ward="N/A",
        date="N/A",
        source_url=BUDGET_MEETING_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Lisa Mpasela",
        role_or_function=(
            "Council Secretary (per the 2023 IDP launch and a 2023-referenced "
            "CDF commissioning news post; a later Council Secretary, Trophius "
            "Kufanga, is documented separately below - exact handover date "
            "not confirmed in available sources)"
        ),
        ward="N/A",
        date="N/A",
        source_url=CDF_EVENT_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Trophius Kufanga",
        role_or_function=(
            "Council Secretary (per the council's Web-Based MIS launch "
            "article; the same individual is separately documented as "
            "Council Secretary at Masaiti Town Council in a 2023 public "
            "notice, consistent with routine inter-council transfer of "
            "council secretaries - exact appointment date to Kalomo not "
            "stated in the source)"
        ),
        ward="N/A",
        date="N/A",
        source_url=MIS_LAUNCH_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Joshua Munsaka Sikaduli",
        role_or_function=(
            "District Commissioner (Office of the President / central "
            "government appointee, not Council staff, but a recurring "
            "civic leader at Council events)"
        ),
        ward="N/A",
        date="N/A",
        source_url=MIS_LAUNCH_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Jimmy Mubanga",
        role_or_function="Director of Finance",
        ward="N/A",
        date="N/A",
        source_url=BUDGET_MEETING_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Joel Mweempe",
        role_or_function="Director of Engineering",
        ward="N/A",
        date="N/A",
        source_url=BUDGET_MEETING_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Judith Beene",
        role_or_function="Director of Information and Communication Technology (ICT)",
        ward="N/A",
        date="N/A",
        source_url=MIS_LAUNCH_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Harry Kamboni",
        role_or_function=(
            "Member of Parliament, Kalomo Central Constituency (national "
            "office, not a Council office; UPND, MP since 2016 per Wikipedia)"
        ),
        ward="N/A",
        date="N/A",
        source_url=WIKIPEDIA_KALOMO_CENTRAL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Valencia Simwale",
        role_or_function=(
            "Vice Council Chairperson; also serves as the Naluja Ward "
            "Councillor (dual role as listed on the Civic Leaders page)"
        ),
        ward="Naluja Ward",
        date="N/A",
        source_url=CIVIC_LEADERS_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Edgar Sing'ombe",
        role_or_function=(
            "Member of Parliament, Dundumwezi Constituency (national "
            "office, not a Council office; UPND, MP since 2006 per Wikipedia, "
            "also named at a Council CDF-project commissioning event)"
        ),
        ward="N/A",
        date="N/A",
        source_url=CDF_EVENT_URL,
    ),

    # --- 2. Departments --------------------------------------------------
    dict(
        record_type="Department",
        name_or_title="Office of the Council Secretary",
        role_or_function=(
            "Administrative leadership and coordination of Council activities; "
            "interprets government policy into implementable programmes"
        ),
        ward="N/A",
        date="N/A",
        source_url=MIS_LAUNCH_URL,
    ),
    dict(
        record_type="Department",
        name_or_title="Finance Department",
        role_or_function="Budget preparation/performance, revenue and expenditure management",
        ward="N/A",
        date="N/A",
        source_url=BUDGET_MEETING_URL,
    ),
    dict(
        record_type="Department",
        name_or_title="Engineering Department",
        role_or_function="Implementation of CDF, ZDSP and Roads Grant infrastructure projects",
        ward="N/A",
        date="N/A",
        source_url=BUDGET_MEETING_URL,
    ),
    dict(
        record_type="Department",
        name_or_title="Information and Communication Technology (ICT) Unit",
        role_or_function="Council digital systems, incl. the Web-Based Management Information System (MIS)",
        ward="N/A",
        date="N/A",
        source_url=MIS_LAUNCH_URL,
    ),

    # --- 3. Ward / Councillor --------------------------------------------
    # Full 20-ward roster from a direct browser view of the Civic Leaders
    # page (2026-09-11) - see source_pages_extract.txt "UPDATE" section.
    # Split into the same two constituencies the page itself uses; totals
    # to 20, matching the district profile's stated ward count.
    *[
        dict(
            record_type="Ward",
            name_or_title=councillor,
            role_or_function="Ward Councillor",
            ward=f"{ward} Ward",
            date="N/A",
            source_url=CIVIC_LEADERS_URL,
        )
        for ward, councillor in [
            # Dundumwezi Constituency (8 wards)
            ("Naluja", "Valencia Simwale"),
            ("Mikata", "Vincent Hamukwala"),
            ("Chamuka", "Patricia Simbeleko"),
            ("Omba", "Willard Hamanjanji"),
            ("Bbilili", "Titus Siamafuwa"),
            ("Kasukwe", "Joel Muleya"),
            ("Chikanta", "Astone Malasha"),
            ("Katanda", "Nkuyanda Malawo"),
            # Kalomo Central Constituency (12 wards)
            ("Namwianga", "David Mutentwa"),
            ("Kalonda", "Denny Moono"),
            ("Chilesha", "Samson Muchimba"),
            ("Chifusa", "Mason Munsanje"),
            ("Nachikungu", "Munsaka Trouble"),
            ("Sipatunyana", "Howard Munsanje"),
            ("Chawila", "Roy Sialubala"),
            ("Siachitema", "Bukoka Milambo"),
            ("Choonga", "Liberty Chifuwe"),
            ("Mayoba", "Lewis Mantanyani"),
            ("Simayakwe", "Miyoba Muloongo"),
            ("Mwaata", "Sialwizi S. Madyenkuku"),
        ]
    ],

    # --- 4. Grassroots governance committees ------------------------------
    dict(
        record_type="Committee",
        name_or_title="Ward Development Committee (WDC)",
        role_or_function=(
            "Grassroots link between communities and the Council; members "
            "elected by ward residents to represent community development "
            "interests. Present in each of the district's 20 wards."
        ),
        ward="All 20 wards",
        date="N/A",
        source_url=FAQS_URL,
    ),
    dict(
        record_type="Committee",
        name_or_title="Community Welfare Assistance Committee (CWAC)",
        role_or_function=(
            "Ward-level committee sensitized/engaged under the Revised Cash "
            "for Work (R-CFW) Programme"
        ),
        ward="All 20 wards",
        date="N/A",
        source_url=RCFW_URL,
    ),
    dict(
        record_type="Committee",
        name_or_title="Satellite Disaster Management Committee (SDMC)",
        role_or_function=(
            "Ward-level disaster-management committee sensitized/engaged "
            "under the Revised Cash for Work (R-CFW) Programme, introduced "
            "in response to the 2023/2024 drought"
        ),
        ward="All 20 wards",
        date="N/A",
        source_url=RCFW_URL,
    ),
    dict(
        record_type="Committee",
        name_or_title="Headmen",
        role_or_function=(
            "Traditional local leaders sensitized/engaged alongside WDCs, "
            "CWACs, SDMCs and councillors under the R-CFW Programme"
        ),
        ward="All 20 wards",
        date="N/A",
        source_url=RCFW_URL,
    ),

    # --- 5. Constituencies -------------------------------------------------
    dict(
        record_type="Constituency",
        name_or_title="Kalomo Central Constituency",
        role_or_function="One of the district's two parliamentary constituencies",
        ward="N/A",
        date="N/A",
        source_url=PROFILE_URL,
    ),
    dict(
        record_type="Constituency",
        name_or_title="Dundumwezi Constituency",
        role_or_function="One of the district's two parliamentary constituencies",
        ward="N/A",
        date="N/A",
        source_url=PROFILE_URL,
    ),

    # --- 6. Chiefdoms -------------------------------------------------------
    dict(
        record_type="Chiefdom",
        name_or_title="Chikanta Chiefdom",
        role_or_function="One of the district's three traditional chiefdoms",
        ward="N/A",
        date="N/A",
        source_url=PROFILE_URL,
    ),
    dict(
        record_type="Chiefdom",
        name_or_title="Siachitema Chiefdom",
        role_or_function="One of the district's three traditional chiefdoms",
        ward="N/A",
        date="N/A",
        source_url=PROFILE_URL,
    ),
    dict(
        record_type="Chiefdom",
        name_or_title="Sipatunyana Chiefdom",
        role_or_function="One of the district's three traditional chiefdoms",
        ward="N/A",
        date="N/A",
        source_url=PROFILE_URL,
    ),
]


def build_rows():
    return list(RECORDS)


def main():
    rows = build_rows()
    df = pd.DataFrame(rows)

    df["record_id"] = [f"AG-{i+1:03d}" for i in range(len(df))]
    df = df[["record_id", "record_type", "name_or_title", "role_or_function",
              "ward", "date", "source_url"]]

    df["date_scraped"] = SCRAPE_DATE

    for col in ["record_type", "name_or_title", "role_or_function", "ward", "date"]:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"": "N/A", "nan": "N/A", "None": "N/A"})

    # Note: subset includes record_type because Valencia Simwale legitimately
    # appears twice (Leadership: Vice Council Chairperson; Ward: Naluja Ward
    # Councillor) - a genuine dual role on the source page, not a duplicate.
    df = df.drop_duplicates(subset=["record_type", "name_or_title", "source_url"]).reset_index(drop=True)

    assert df["source_url"].str.startswith("https://").all(), "every row must have a working https source_url"
    assert not df["record_id"].duplicated().any(), "record_id must be unique"

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, sep="|", index=False)
    print(f"Wrote {len(df)} rows to {OUT_PATH}")
    print(df[["record_id", "record_type", "name_or_title", "role_or_function"]].to_string(index=False))


if __name__ == "__main__":
    main()
