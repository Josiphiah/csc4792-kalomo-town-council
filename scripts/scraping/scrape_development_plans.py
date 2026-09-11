"""
Scrape development-plan documents (IDPs, strategic plans, sector/community
project plans) published on the Kalomo Town Council website.

The council's WordPress site does not have a single "Development Plans"
menu item. Its planning documents are split across two places:

  1. The "ZDSP" page (Zambia Devolution Support Programme) at ?page_id=3889,
     which has a "KEY DOCUMENTS" list of PDFs.
  2. The "Publications" page at ?page_id=4451, which uses tabs (rendered as
     hidden <div> blocks in the page HTML, all present even though only one
     tab is visible at a time in the browser) including an "IDP" tab,
     "Investment Profile" tab, "Procurement Plan" tab and "Engagement Plan"
     tab, each linking to PDFs.

This script fetches both pages, pulls every PDF link out of the relevant
sections, downloads each PDF into data/raw/development_plans/pdfs/, and
extracts its text (where the PDF has a real text layer) into a companion
"<name>_extract.txt" file in data/raw/development_plans/ for manual review
in the cleaning step.
"""

import os
import time

import requests
import urllib3
from bs4 import BeautifulSoup
import pdfplumber

# The council's site serves an incomplete/misconfigured TLS certificate
# chain (confirmed independently with curl -v), which fails standard
# certificate verification even though the site itself is legitimate and
# publicly reachable in a browser. We disable verification only for this
# specific government host and silence the resulting warning; no
# credentials are ever sent, so this only affects tamper-detection on
# these public, unauthenticated GET requests.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {"User-Agent": "Mozilla/5.0 (Student research project - CSC4792 UNZA)"}
BASE = "https://www.kalomocouncil.gov.zm"

RAW_DIR = os.path.join("data", "raw", "development_plans")
PDF_DIR = os.path.join(RAW_DIR, "pdfs")

# Pages known (from manually browsing the site first) to list planning /
# strategic / investment documents relevant to this dataset.
SOURCE_PAGES = [
    f"{BASE}/?page_id=3889",   # ZDSP -> "KEY DOCUMENTS"
    f"{BASE}/?page_id=4451",   # Publications -> IDP / Investment Profile /
                                # Procurement Plan / Engagement Plan tabs
]

# Only these documents are in scope for the *development plans* dataset.
# (Publications also lists Financial Statements, Minutes, Acts & Policies,
# etc. which belong to Faiz's financial dataset or Nicholas's governance
# dataset instead, so we deliberately filter to planning-related PDFs.)
RELEVANT_KEYWORDS = [
    "idp", "investment", "zdsp", "decentralisation", "engagement",
    "procurement", "esmp", "debt-arrears", "citizen_engagement",
]


def get_soup(url):
    r = requests.get(url, headers=HEADERS, timeout=20, verify=False)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def find_pdf_links(soup, base_url):
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".pdf"):
            text = a.get_text(strip=True) or os.path.basename(href)
            links.append({"text": text, "url": href, "page": base_url})
    return links


def is_relevant(link):
    haystack = (link["text"] + " " + link["url"]).lower()
    return any(kw in haystack for kw in RELEVANT_KEYWORDS)


def download_pdf(url, dest_path):
    r = requests.get(url, headers=HEADERS, timeout=60, verify=False)
    r.raise_for_status()
    with open(dest_path, "wb") as f:
        f.write(r.content)


def extract_text(pdf_path, txt_path, max_pages=20):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = pdf.pages[:max_pages]
            text = "\n".join(p.extract_text() or "" for p in pages)
    except Exception as exc:  # scanned/corrupt PDFs shouldn't kill the run
        text = ""
        print(f"  ! could not extract text from {pdf_path}: {exc}")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)
    return len(text.strip())


def main():
    os.makedirs(PDF_DIR, exist_ok=True)
    all_links = []

    for page_url in SOURCE_PAGES:
        print(f"Fetching {page_url} ...")
        soup = get_soup(page_url)
        links = find_pdf_links(soup, page_url)
        relevant = [l for l in links if is_relevant(l)]
        print(f"  found {len(links)} PDF links, {len(relevant)} relevant")
        all_links.extend(relevant)
        time.sleep(1)  # be polite to the council's server

    # de-duplicate by URL (the "Citizen Engagement Strategy" PDF, for
    # example, is linked from both source pages)
    seen = set()
    unique_links = []
    for link in all_links:
        if link["url"] not in seen:
            seen.add(link["url"])
            unique_links.append(link)

    print(f"\n{len(unique_links)} unique relevant PDFs to download:\n")
    for link in unique_links:
        fname = os.path.basename(link["url"]).split("?")[0]
        pdf_path = os.path.join(PDF_DIR, fname)
        txt_path = os.path.join(RAW_DIR, fname.replace(".pdf", "_extract.txt"))

        print(f"- {link['text']} ({link['url']})")
        download_pdf(link["url"], pdf_path)
        chars = extract_text(pdf_path, txt_path)
        status = f"{chars} chars extracted" if chars else "no extractable text (scanned/image PDF)"
        print(f"  -> saved {fname}, {status}")
        time.sleep(1)


if __name__ == "__main__":
    main()
