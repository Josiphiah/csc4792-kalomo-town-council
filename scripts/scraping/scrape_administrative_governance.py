"""
Scrape administrative/governance data (leadership, departments, wards,
Ward Development Committees, and related grassroots governance structures)
from the Kalomo Town Council website.

Unlike the development-plans dataset (a handful of downloadable PDFs), this
data lives in ordinary HTML pages spread across the site plus individual
news posts. The pages known (from manually browsing the site) to carry
administrative/governance content are listed in SOURCE_PAGES below.

Note on connectivity: the council's site returned HTTP 403 to a plain
`requests.get` from the sandboxed environment used to build this repo, and
is robots-disallowed for hosted fetch tools generally - the same TLS/
access quirks noted in scrape_development_plans.py. From a normal
unrestricted connection (e.g. a teammate's laptop, as used for the other
three datasets in this project) this script will fetch and save the raw
HTML directly, which is what happens below. Where that wasn't possible in
this session, the equivalent content was instead compiled by hand into
data/raw/administrative_governance/source_pages_extract.txt from indexed
copies of the same pages - documented there per source, following the same
"record what's actually available, note the gaps" approach used for the
scanned PDFs in the development-plans dataset. Re-running this script from
an unrestricted connection will populate this folder with the full raw
HTML/JSON and should be preferred over the manual notes where possible.
"""

import json
import os
import time

import requests
import urllib3
from bs4 import BeautifulSoup

# See scrape_development_plans.py for why verify=False is used here: the
# council's site serves an incomplete TLS chain that fails standard
# verification even though the site is legitimate and publicly reachable
# in a browser. No credentials are ever sent; only public, unauthenticated
# GET requests are made.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {"User-Agent": "Mozilla/5.0 (Student research project - CSC4792 UNZA)"}
BASE = "https://www.kalomocouncil.gov.zm"

RAW_DIR = os.path.join("data", "raw", "administrative_governance")

# Pages/posts known to carry leadership, department, ward, WDC or related
# governance content for this dataset (see source_pages_extract.txt for
# what each one contains).
SOURCE_PAGES = {
    "about_us": f"{BASE}/?page_id=118",
    "district_profile": f"{BASE}/?page_id=2242",
    "civic_leaders": f"{BASE}/?page_id=2871",
    "departments": f"{BASE}/?page_id=770",
    "faqs": f"{BASE}/?page_id=2259",
    "news_index": f"{BASE}/?page_id=187",
    "news_cdf_equipment_commissioning": f"{BASE}/?p=1799",
    "news_2026_budget_consultative_meeting": f"{BASE}/?p=3782",
    "news_mis_launch": f"{BASE}/?p=4672",
    "news_cash_for_work_sensitization": f"{BASE}/?p=5104",
}


def fetch_page(name, url):
    r = requests.get(url, headers=HEADERS, timeout=20, verify=False)
    r.raise_for_status()
    return r.text


def extract_visible_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    results = {}

    for name, url in SOURCE_PAGES.items():
        print(f"Fetching {name} ({url}) ...")
        try:
            html = fetch_page(name, url)
        except requests.RequestException as exc:
            print(f"  ! could not fetch {url}: {exc}")
            print("  -> falling back to manual notes in "
                  "source_pages_extract.txt for this page")
            results[name] = {"url": url, "status": "fetch_failed", "error": str(exc)}
            time.sleep(1)
            continue

        html_path = os.path.join(RAW_DIR, f"{name}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        text = extract_visible_text(html)
        txt_path = os.path.join(RAW_DIR, f"{name}_extract.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        results[name] = {"url": url, "status": "ok", "chars_extracted": len(text)}
        print(f"  -> saved {name}.html and {name}_extract.txt "
              f"({len(text)} chars)")
        time.sleep(1)  # be polite to the council's server

    manifest_path = os.path.join(RAW_DIR, "fetch_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote fetch manifest to {manifest_path}")


if __name__ == "__main__":
    main()
