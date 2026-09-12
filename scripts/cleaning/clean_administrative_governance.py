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
INSTITUTIONAL_MGMT_URL = "https://www.kalomocouncil.gov.zm/?page_id=3964"
FOOD_SECURITY_PACK_URL = "https://www.kalomocouncil.gov.zm/?p=2014"
SERVICES_URL = "https://www.kalomocouncil.gov.zm/?page_id=792"
WIKIPEDIA_KALOMO_CENTRAL = "https://en.wikipedia.org/wiki/Kalomo_Central"
WIKIPEDIA_DUNDUMWENZI = "https://en.wikipedia.org/wiki/Dundumwenzi_(constituency)"

FOOTER_URL = "https://www.kalomocouncil.gov.zm/?page_id=770"  # captured from the site-wide footer

# Uploaded scanned council documents (not from the website - user-supplied
# primary sources). No public URL exists for these, so source_url records
# the document title/date instead, consistent with how a physical/scanned
# source with no URL should be cited when a URL genuinely doesn't exist.
DUNDUMWEZI_CDF_MINUTES_URL = "Dundumwezi CDF Committee Minutes, 29 December 2023 (uploaded scan, no public URL)"
KALOMO_CENTRAL_CDF_MINUTES_URL = "Kalomo Central CDF Committee Minutes, 9-10 February 2024 (uploaded scan, no public URL)"
BUDGET_ENGAGEMENT_MINUTES_URL = "Community Engagement Meeting Minutes on Budget Preparation, 28 November 2024 (uploaded scan, no public URL)"

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
        role_or_function=(
            "Director of Engineering (per the 2026 budget consultative "
            "meeting post). Also appears, spelled \"Joel Mwempe\" and "
            "titled \"Ass. Director of Engineering Services\", in the "
            "28 Nov 2024 Community Engagement Meeting minutes - same "
            "person, spelling/title varies slightly by document"
        ),
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
            "The Council Secretary is the Chief Executive Officer "
            "responsible for overseeing Council operations, providing "
            "overall policy guidance and oversight, and ensuring "
            "effective linkages among and within Departments/Units "
            "(per the Institutional Management page, headed by "
            "Trophius Kufanga)"
        ),
        ward="N/A",
        date="N/A",
        source_url=INSTITUTIONAL_MGMT_URL,
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
        name_or_title="Department of Community Development and Social Services",
        role_or_function=(
            "Administers social support programmes, e.g. handed over "
            "farming equipment/livestock to beneficiaries under the Food "
            "Security Pack Program (news post dated 11 September 2024)"
        ),
        ward="N/A",
        date="2024-09-11",
        source_url=FOOD_SECURITY_PACK_URL,
    ),
    dict(
        record_type="Department",
        name_or_title="Legal Services Unit",
        role_or_function=(
            "Unit within the Office of the Council Secretary; provides "
            "legal advice and safeguards the Council's interests. Headed "
            "by a Council Advocate, assisted by 2 Senior Legal Assistants"
        ),
        ward="N/A",
        date="N/A",
        source_url=INSTITUTIONAL_MGMT_URL,
    ),
    dict(
        record_type="Department",
        name_or_title="Procurement and Supplies Unit",
        role_or_function=(
            "Unit within the Office of the Council Secretary; procures "
            "works, goods and services for value for money and efficient "
            "use of Council resources"
        ),
        ward="N/A",
        date="N/A",
        source_url=INSTITUTIONAL_MGMT_URL,
    ),
    dict(
        record_type="Department",
        name_or_title="Public Relations Unit",
        role_or_function=(
            "Unit within the Office of the Council Secretary; informs the "
            "public and enhances the Council's image"
        ),
        ward="N/A",
        date="N/A",
        source_url=INSTITUTIONAL_MGMT_URL,
    ),
    dict(
        record_type="Department",
        name_or_title="Internal Audit Unit",
        role_or_function=(
            "Unit within the Office of the Council Secretary; manages the "
            "internal audit function and oversight of public resources"
        ),
        ward="N/A",
        date="N/A",
        source_url=INSTITUTIONAL_MGMT_URL,
    ),
    dict(
        record_type="Department",
        name_or_title="Information and Communication Technology (ICT) Unit",
        role_or_function=(
            "Unit within the Office of the Council Secretary; manages and "
            "supports the Council's technology systems"
        ),
        ward="N/A",
        date="N/A",
        source_url=INSTITUTIONAL_MGMT_URL,
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
        date="2026-06-16",
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
        date="2026-06-16",
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
        date="2026-06-16",
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

    # --- 7. Services ----------------------------------------------------------
    dict(
        record_type="Service",
        name_or_title="Council Services (Services page overview)",
        role_or_function=(
            "Refuse collection (Keep Zambia Clean, Green and Healthy "
            "campaign); borehole drilling for clean water; procurement via "
            "the Electronic Government Procurement (e-GP) system; feeder-"
            "road provision through the Engineering Department; HIV/AIDS, "
            "gender and human rights sensitisation; licensing services "
            "(trade licences, health permit licences, liquor licences - "
            "issuing department/unit not stated in the source)"
        ),
        ward="N/A",
        date="N/A",
        source_url=SERVICES_URL,
    ),

    # --- 8. Constituency Development Fund Committees (CDFC) ---------------
    # Formal governance committees, confirmed via uploaded scanned minutes
    # (not on the public website). Membership as printed in each minutes
    # document.
    dict(
        record_type="Committee",
        name_or_title="Dundumwezi Constituency Development Fund Committee (CDFC)",
        role_or_function=(
            "Chairperson: Simon Chikonka. Members: Febias Simisamu, Staff "
            "Hakumbila, Happiness Kaande, Patricia Simbeleko, Ebby Kapepe, "
            "Adron Mudenda, and MP Edgar Sing'ombe. Reviews and resolves on "
            "CDF community project applications and fund allocation for "
            "Dundumwezi Constituency (per minutes of the meeting held 29 "
            "December 2023)"
        ),
        ward="N/A",
        date="2023-12-29",
        source_url=DUNDUMWEZI_CDF_MINUTES_URL,
    ),
    dict(
        record_type="Committee",
        name_or_title="Kalomo Central Constituency Development Fund Committee (CDFC)",
        role_or_function=(
            "Chairperson: Siyunyi Katanekwa. Members: Moses M Hamoonga, "
            "Sialubala Roy, Michael Chinganya, Mason Musanje, Sialwizi S. "
            "Madyenkuku, Dickson Simbweede, and MP Harry Kamboni. Reviews "
            "and resolves on CDF community project applications and fund "
            "allocation for Kalomo Central Constituency (per minutes of "
            "the meeting held 9-10 February 2024)"
        ),
        ward="N/A",
        date="2024-02-09",
        source_url=KALOMO_CENTRAL_CDF_MINUTES_URL,
    ),

    # --- 9. Named Ward Development Committee (WDC) Chairpersons -----------
    # From the attendance list of the 28 Nov 2024 Community Engagement
    # Meeting on Budget Preparation - the first time named individuals were
    # confirmed per ward (vs. the generic WDC-are-present-in-every-ward
    # record already logged under Committee above). Two names come from the
    # meeting's "Apologies" list (absent that day, but named as the sitting
    # WDC Chairperson for their ward, per the minutes).
    *[
        dict(
            record_type="Committee",
            name_or_title=f"Ward Development Committee (WDC) Chairperson - {ward} Ward",
            role_or_function=f"WDC Chairperson: {name}",
            ward=f"{ward} Ward",
            date="2024-11-28",
            source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
        )
        for ward, name in [
            ("Katanda", "Jeremiah Muyangana"),
            ("Choonga", "Clayford Hakooba"),
            ("Naluja", "Paul Hamweemba"),
            ("Namwianga", "Costene Chiyumba"),
            ("Simayakwe", "Mercy Chilundika"),
            ("Sipatunyana", "Winter Moono"),
            ("Chilesha", "Jerald Makaya"),
            ("Bbilili", "Albertina Habuluba"),
            ("Nachikungu", "Patient Munyandi"),
            ("Kalonda", "Allan Kanenga"),
            ("Siachitema", "Nakambowa Songiso"),
            ("Chikanta", "Stanley Nalube"),
            ("Mayoba", "Abion Muntanga"),  # listed under Apologies (absent)
            ("Chawila", "Payford Dabali"),  # listed under Apologies (absent)
        ]
    ],
    dict(
        record_type="Committee",
        name_or_title="Ruth M. Langisi",
        role_or_function=(
            "Listed on the attendance sheet simply as \"WDC-Mwaata\" - "
            "likely a WDC representative for Mwaata Ward, but the source "
            "does not explicitly state \"Chairperson\" (unlike the 14 "
            "entries above that do), so that title is not assumed here"
        ),
        ward="Mwaata Ward",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),

    # --- 10. Additional council leadership/staff confirmed via minutes -----
    dict(
        record_type="Leadership",
        name_or_title="Choolwe Hachija",
        role_or_function="Chief Accountant, Kalomo Town Council",
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Mary Muponda",
        role_or_function="Public Relations Officer (heads the Public Relations Unit logged above)",
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Bridget Mweetwa",
        role_or_function="Internal Auditor (heads the Internal Audit Unit logged above)",
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Siabona Gamitto",
        role_or_function="Council Advocate (heads the Legal Services Unit logged above)",
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Muchula Maboshe",
        role_or_function="Chief Administrative and Committee Officer",
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Janet Chilala",
        role_or_function=(
            "Senior Committee Clerk (listed as \"Ag. Snr Committee Clerk\" "
            "in the Dec 2023 Dundumwezi CDF minutes and \"Committee Clerk\" "
            "in the Feb 2024 Kalomo Central CDF minutes - same person, "
            "title varies slightly by document)"
        ),
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Nchimunya Saasa",
        role_or_function="Committee Clerk",
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Gideon Lengwe",
        role_or_function="Valuation Officer",
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Bosco Kapopo",
        role_or_function=(
            "Community Development Officer (part of the Department of "
            "Community Development and Social Services logged above)"
        ),
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Miranda Muleya",
        role_or_function=(
            "Ag. District Planning Officer (Secretariat) - appears across "
            "all three uploaded CDF/budget meeting minutes (Dec 2023, Feb "
            "2024, Nov 2024) as the compiling/secretariat officer"
        ),
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Christopher Zyambo",
        role_or_function=(
            "Council/District Treasurer (titled \"District Treasurer\" in "
            "the Dec 2023 Dundumwezi minutes and \"Council Treasure[r]\" "
            "in the Feb 2024 Kalomo Central minutes - same person)"
        ),
        ward="N/A",
        date="2024-02-09",
        source_url=KALOMO_CENTRAL_CDF_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Chikumbuso Banda",
        role_or_function="Director of Works",
        ward="N/A",
        date="2024-02-09",
        source_url=KALOMO_CENTRAL_CDF_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Rose Chulu",
        role_or_function="Socio-Economic Planner",
        ward="N/A",
        date="2024-02-09",
        source_url=KALOMO_CENTRAL_CDF_MINUTES_URL,
    ),
    dict(
        record_type="Leadership",
        name_or_title="Wallace Hamasuku",
        role_or_function="Assistant Community Development Officer",
        ward="N/A",
        date="2024-02-09",
        source_url=KALOMO_CENTRAL_CDF_MINUTES_URL,
    ),

    # --- 11. Resolutions (curated - selected governance-level resolutions
    # from the three uploaded minutes documents. Detailed CDF project-level
    # tables and financial performance figures in these same documents are
    # deliberately NOT duplicated here - that level of detail belongs in
    # the team's separate cdf_projects and financial_data datasets, not
    # administrative_governance. See source_pages_extract.txt for the note
    # flagging this to those dataset owners.) --------------------------------
    dict(
        record_type="Resolution",
        name_or_title="CDFKALDUN/07/11/23: Adoption of CDF Minutes",
        role_or_function="Resolved: the Dundumwezi CDF minutes held 29 November 2023 be adopted as a true record of proceedings",
        ward="N/A",
        date="2023-12-29",
        source_url=DUNDUMWEZI_CDF_MINUTES_URL,
    ),
    dict(
        record_type="Resolution",
        name_or_title="CDFKALDUN/14/12/23: Empowerment Loan Application for 2024",
        role_or_function="Resolved: each ward be allocated K400,000.00 for empowerment loans; committee members to select successful applicants",
        ward="All wards (Dundumwezi Constituency)",
        date="2023-12-29",
        source_url=DUNDUMWEZI_CDF_MINUTES_URL,
    ),
    dict(
        record_type="Resolution",
        name_or_title="CDFKALDUN/14/15/23: Secondary School Boarding and Skills Development Applications for 2024",
        role_or_function=(
            "Resolved: 164 Secondary Boarding School applicants and 117 "
            "Skills Development Training applicants approved; all "
            "applications to Nsenje Hills Training Institute withdrawn "
            "(overly priced tuition) and all to Mufurila Training "
            "Institute withdrawn (students denied food despite payment)"
        ),
        ward="All wards (Dundumwezi Constituency)",
        date="2023-12-29",
        source_url=DUNDUMWEZI_CDF_MINUTES_URL,
    ),
    dict(
        record_type="Resolution",
        name_or_title="CDFKALCEN/02/02/24: Adoption of CDF Minutes",
        role_or_function="Resolved: the CDF Central minutes held 23 November 2023 be adopted as a true record of proceedings, with amendments",
        ward="N/A",
        date="2024-02-09",
        source_url=KALOMO_CENTRAL_CDF_MINUTES_URL,
    ),
    dict(
        record_type="Resolution",
        name_or_title="CDFKALCEN/03/02/24: Amendment of 2024 Proposed Projects",
        role_or_function=(
            "Resolved: a 33-project list for Kalomo Central Constituency "
            "approved with amended funding amounts, totalling "
            "K16,589,200.12 (full project-level detail intentionally not "
            "duplicated here - see the team's cdf_projects dataset)"
        ),
        ward="All wards (Kalomo Central Constituency)",
        date="2024-02-09",
        source_url=KALOMO_CENTRAL_CDF_MINUTES_URL,
    ),
    dict(
        record_type="Resolution",
        name_or_title="CES/05/11/24: Submission of Proposed Projects for 2025 (ZDSP)",
        role_or_function=(
            "Resolved: 6 projects approved for Zambia Devolution Support "
            "Programme (ZDSP) funding - Trucking Bay (Kalomo Central), "
            "Solar Street Lights along T1 Phase II, Dump site fencing, "
            "Refuse Bays (5 markets), Police Post Staff House at Kasukwe "
            "(Dundumwezi), Water Irrigation Scheme at Mukwela (Kalomo "
            "Central)"
        ),
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
    ),

    # --- 12. Reports --------------------------------------------------------
    dict(
        record_type="Report",
        name_or_title="Community Engagement Meeting Minutes on Budget Preparation",
        role_or_function=(
            "Director of Finance presented 2024 budget performance (76% "
            "overall collection efficiency against the approved annual "
            "budget) and the proposed 2025 budget (K156.3 million, a 63% "
            "increase over 2024, driven by the new Cash for Work Fund and "
            "increased CDF). Detailed revenue/expenditure figures "
            "intentionally not duplicated here - see the team's "
            "financial_data dataset"
        ),
        ward="N/A",
        date="2024-11-28",
        source_url=BUDGET_ENGAGEMENT_MINUTES_URL,
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

    # Most rows cite a live https:// page; a handful cite an uploaded scanned
    # document that has no public URL (see the *_MINUTES_URL constants above) -
    # those are allowed too, but every row must have a real, non-empty source.
    valid_source = df["source_url"].str.startswith("https://") | df["source_url"].str.contains("uploaded scan, no public URL")
    assert valid_source.all(), "every row must cite either a working https source_url or a clearly-labelled uploaded document"
    assert not df["record_id"].duplicated().any(), "record_id must be unique"

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, sep="|", index=False)
    print(f"Wrote {len(df)} rows to {OUT_PATH}")
    print(df[["record_id", "record_type", "name_or_title", "role_or_function"]].to_string(index=False))


if __name__ == "__main__":
    main()
