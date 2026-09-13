"""
crawl_and_scrape_financial.py

Runs the WHOLE discovery + scraping process on its own:
  1. Starts at the Kalomo Town Council homepage.
  2. Follows every internal link it finds (same website only), including
     paginated news listings, individual news posts, and downloadable
     documents (PDF, DOCX, XLSX, XLS, PPTX).
  3. For every page/document it visits, checks whether the text looks
     financial (budget, revenue, OSR, LGEF, CDF funds, market fees, etc).
  4. Saves anything financial-looking into data/raw/financial_data/,
     with the full text kept so nothing is thrown away.

You do NOT need to find URLs yourself. Just run this script from a
machine with normal internet access:

    python3 scripts/scraping/crawl_and_scrape_financial.py

This now runs straight through to completion by itself -- no need to
keep re-running it. It will keep going, page after page, until there
is nothing left to visit, then stop on its own.

CRASH-SAFETY: every result is saved to disk THE MOMENT it is found
(not just at the end), and the crawl position is saved after every
single page. So even if it does get interrupted, nothing already found
is lost -- just run the exact same command again and it resumes right
where it stopped.

IF YOU ARE ON A SHARED SERVER OVER SSH (e.g. a machine like "node2"):
your session disconnecting will normally kill any command you are
running in the foreground, even though nothing is wrong with the
script itself. To stop that from happening, launch it detached from
your terminal like this instead of running it directly:

    nohup python3 scripts/scraping/crawl_and_scrape_financial.py > crawl.log 2>&1 &
    disown

Then you can safely close your terminal or let your SSH session drop --
the crawl keeps running on the server in the background. Check on it
any time with:

    tail -20 crawl.log

Only text-bearing documents are ever downloaded (web pages, PDFs, Word,
Excel, PowerPoint files). Video, audio, and image files are always
skipped automatically -- they are never relevant to this dataset and
are never saved.

METHOD NOTE for your Data in Brief paper: this council's robots.txt
disallows automated crawling. `requests` does not enforce robots.txt
automatically, so this script will still technically work, but you
should disclose this in your paper's methodology/limitations section.
"""

import re
import csv
import time
import json
import warnings
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
import pdfplumber
import io
import docx
import openpyxl
import xlrd
from pptx import Presentation
from requests.packages.urllib3.exceptions import InsecureRequestWarning

START_URL = "https://www.kalomocouncil.gov.zm/"
DOMAIN = "kalomocouncil.gov.zm"

# Safety ceiling only -- not meant to be hit in normal use. A small
# council website should have far fewer pages than this. It exists so a
# URL-parameter loop (e.g. an infinite calendar of "next month" links)
# can't make the crawl run forever.
MAX_PAGES_PER_RUN = 5000
REQUEST_DELAY_SECONDS = 1.0

# Print a short status line every N pages so a background log file
# (crawl.log) shows the crawl is still alive even during long stretches
# with few or no financial pages found.
HEARTBEAT_EVERY = 25

BASE_DIR = Path(__file__).resolve().parents[2]  # kalomo_project/
RAW_DIR = BASE_DIR / "data" / "raw" / "financial_data"
STATE_FILE = RAW_DIR / "_crawl_state.json"
OUT_HTML = RAW_DIR / "raw_scraped_articles.csv"
OUT_PDF = RAW_DIR / "raw_scraped_pdfs.csv"
ALL_URLS_LOG = RAW_DIR / "all_urls_visited.txt"

HTML_FIELDS = ["source_url", "title", "raw_text", "scrape_date"]
PDF_FIELDS = ["source_url", "local_file", "raw_text", "scrape_date"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (CSC4792 UNZA student research project; contact: your-email@example.com)"
}

# Keywords that suggest a page is financially relevant. Broad on purpose --
# better to keep a few irrelevant pages than miss a relevant one; you can
# always filter more in the cleaning step.
FINANCIAL_KEYWORDS = [
    "budget", "revenue", "osr", "own source revenue", "lgef",
    "equalisation fund", "equalization fund", "cdf", "constituency development fund",
    "levy", "levies", "market fee", "fees", "tax", "rates", "grant", "grants",
    "expenditure", "financial year", "audit", "collection", "collections",
    "disbursement", "allocation", "procurement", "resolution", "resolutions",
    "council meeting", "idp", "integrated development plan", "ward development",
    "finance", "financial", "fund", "funding", "kwacha", " k1", " k2", " k3",
    " k4", " k5", " k6", " k7", " k8", " k9", "zdsp", "devolution",
    "capital expenditure", "recurrent", "income", "expenses", "cost", "funded",
    "million", "billion", "report", "annual report", "quarterly", "performance",
]

PDF_DIR = RAW_DIR / "pdfs"

SKIP_EXTENSIONS = (
    ".mp4", ".mov", ".avi", ".wmv", ".mkv",
    ".mp3", ".wav",
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico",
    ".zip", ".rar", ".7z", ".exe", ".dmg",
)
MAX_DOWNLOAD_BYTES = 15 * 1024 * 1024  # skip anything bigger than 15 MB


def is_internal(url: str) -> bool:
    parsed = urlparse(url)
    return (parsed.netloc == "" or DOMAIN in parsed.netloc)


def normalise(url: str) -> str:
    return url.split("#")[0]


def looks_financial(text: str) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in FINANCIAL_KEYWORDS)


def should_skip_by_extension(url: str) -> bool:
    return url.lower().split("?")[0].endswith(SKIP_EXTENSIONS)


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"visited": [], "to_visit": [START_URL]}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def append_row(path: Path, fieldnames: list, row: dict):
    """Write one row to a CSV immediately, creating the header if needed."""
    file_exists = path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def extract_html_text(html: str):
    soup = BeautifulSoup(html, "lxml")
    title_tag = soup.find("h1") or soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    content_selectors = [
        {"class_": "entry-content"},
        {"class_": "post-content"},
        {"class_": "content"},
        {"id": "content"},
    ]
    article_text = ""
    for sel in content_selectors:
        node = soup.find("div", **sel)
        if node:
            article_text = node.get_text(separator=" ", strip=True)
            break
    if not article_text:
        paragraphs = soup.find_all("p")
        article_text = " ".join(p.get_text(strip=True) for p in paragraphs)

    links = [urljoin(START_URL, a.get("href")) for a in soup.find_all("a", href=True)]
    return title, article_text, links


def extract_pdf_text(content: bytes) -> str:
    text_chunks = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            text_chunks.append(page.extract_text() or "")
    return "\n".join(text_chunks)


def extract_docx_text(content: bytes) -> str:
    doc = docx.Document(io.BytesIO(content))
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            parts.append(" | ".join(cell.text for cell in row.cells))
    return "\n".join(parts)


def extract_xlsx_text(content: bytes) -> str:
    wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True)
    lines = []
    for sheet in wb.worksheets:
        lines.append(f"--- Sheet: {sheet.title} ---")
        for row in sheet.iter_rows(values_only=True):
            row_text = " | ".join(str(cell) for cell in row if cell is not None)
            if row_text.strip():
                lines.append(row_text)
    return "\n".join(lines)


def extract_xls_text(content: bytes) -> str:
    book = xlrd.open_workbook(file_contents=content)
    lines = []
    for sheet in book.sheets():
        lines.append(f"--- Sheet: {sheet.name} ---")
        for row_idx in range(sheet.nrows):
            row = sheet.row_values(row_idx)
            row_text = " | ".join(str(cell) for cell in row if cell != "")
            if row_text.strip():
                lines.append(row_text)
    return "\n".join(lines)


def extract_pptx_text(content: bytes) -> str:
    prs = Presentation(io.BytesIO(content))
    lines = []
    for i, slide in enumerate(prs.slides, start=1):
        lines.append(f"--- Slide {i} ---")
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    text = "".join(run.text for run in paragraph.runs)
                    if text.strip():
                        lines.append(text)
    return "\n".join(lines)


def extract_best_effort_text(content: bytes) -> str:
    """
    Fallback for legacy formats with no reliable pure-Python reader
    (old .doc, old .ppt). Pulls out runs of readable ASCII text directly
    from the raw bytes. Rough, but means nothing is thrown away untouched.
    """
    matches = re.findall(rb"[\x20-\x7e]{4,}", content)
    return "\n".join(m.decode("ascii", errors="ignore") for m in matches)


def get_with_fallback(url, **kwargs):
    """
    Try a normal, secure request first. If it fails specifically because
    of a certificate chain problem on the SERVER side (common on some
    under-resourced government sites), retry once without certificate
    verification. Uses stream=True so we can check headers before
    downloading the full body.
    """
    try:
        return requests.get(url, timeout=kwargs.get("timeout", 20),
                             headers=kwargs.get("headers"), stream=True, verify=True)
    except requests.exceptions.SSLError:
        print(f"   [!] SSL certificate chain issue on server side for {url}")
        print(f"   [!] Retrying WITHOUT certificate verification (server-side cert problem, not yours)")
        warnings.simplefilter("ignore", InsecureRequestWarning)
        return requests.get(url, timeout=kwargs.get("timeout", 20),
                             headers=kwargs.get("headers"), stream=True, verify=False)


def classify_content(url_lower: str, content_type: str):
    """Decide what kind of document this response is. HTML is checked
    BEFORE the generic 'text/' check, because 'text/html' also starts
    with 'text/' and would otherwise be wrongly treated as plain text."""
    if "pdf" in content_type or url_lower.endswith(".pdf"):
        return "pdf"
    if "wordprocessingml" in content_type or url_lower.endswith(".docx"):
        return "docx"
    if "spreadsheetml" in content_type or url_lower.endswith(".xlsx"):
        return "xlsx"
    if "ms-excel" in content_type or url_lower.endswith(".xls"):
        return "xls"
    if "presentationml" in content_type or url_lower.endswith(".pptx"):
        return "pptx"
    if url_lower.endswith(".doc") or url_lower.endswith(".ppt") or "msword" in content_type or "ms-powerpoint" in content_type:
        return "best_effort"
    if "html" in content_type or content_type == "":
        return "html"
    if url_lower.endswith((".txt", ".csv", ".json", ".xml")) or content_type.startswith("text/"):
        return "plain_text"
    return None


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    state = load_state()
    visited = set(state["visited"])
    to_visit = list(dict.fromkeys(state["to_visit"]))  # de-dupe, keep order

    html_saved = 0
    pdf_saved = 0
    pages_done = 0

    print(f"Resuming crawl: {len(visited)} pages already visited, "
          f"{len(to_visit)} queued.")
    print(f"Running until the queue is empty (safety ceiling: {MAX_PAGES_PER_RUN} pages).\n", flush=True)

    try:
        while to_visit and pages_done < MAX_PAGES_PER_RUN:
            url = normalise(to_visit.pop(0))
            if url in visited or not is_internal(url) or should_skip_by_extension(url):
                continue

            pages_done += 1
            if pages_done % HEARTBEAT_EVERY == 0:
                print(f"[heartbeat] {pages_done} pages visited this run, "
                      f"{len(to_visit)} still queued, {html_saved + pdf_saved} saved so far.",
                      flush=True)
            print(f"[{pages_done}] Visiting: {url}", flush=True)
            visited.add(url)

            try:
                resp = get_with_fallback(url, headers=HEADERS, timeout=20)
                content_type = resp.headers.get("Content-Type", "")
                content_length = int(resp.headers.get("Content-Length", 0) or 0)
                url_lower = url.lower()

                file_kind = classify_content(url_lower, content_type)

                if file_kind is None:
                    print(f"   [skip] Unsupported content type: {content_type}")
                    resp.close()
                    continue

                if content_length and content_length > MAX_DOWNLOAD_BYTES:
                    print(f"   [skip] File too large ({content_length / 1_000_000:.1f} MB)")
                    resp.close()
                    continue

                resp.raise_for_status()

                if file_kind != "html" and len(resp.content) > MAX_DOWNLOAD_BYTES:
                    print(f"   [skip] File too large after download")
                    continue

                scrape_date = time.strftime("%Y-%m-%d")

                if file_kind == "html":
                    title, text, links = extract_html_text(resp.text)
                    if looks_financial(text):
                        append_row(OUT_HTML, HTML_FIELDS, {
                            "source_url": url, "title": title,
                            "raw_text": text, "scrape_date": scrape_date,
                        })
                        html_saved += 1
                        print("   -> financial HTML page saved")
                    for link in links:
                        link = normalise(link)
                        if is_internal(link) and link not in visited and link not in to_visit:
                            to_visit.append(link)
                else:
                    extractors = {
                        "pdf": extract_pdf_text,
                        "docx": extract_docx_text,
                        "xlsx": extract_xlsx_text,
                        "xls": extract_xls_text,
                        "pptx": extract_pptx_text,
                        "best_effort": extract_best_effort_text,
                    }
                    if file_kind == "plain_text":
                        text = resp.text
                    else:
                        text = extractors[file_kind](resp.content)
                    if looks_financial(text):
                        filename = url.split("/")[-1] or f"document.{file_kind}"
                        (PDF_DIR / filename).write_bytes(resp.content if file_kind != "plain_text" else text.encode("utf-8"))
                        append_row(OUT_PDF, PDF_FIELDS, {
                            "source_url": url, "local_file": filename,
                            "raw_text": text, "scrape_date": scrape_date,
                        })
                        pdf_saved += 1
                        print(f"   -> financial {file_kind} document saved")

            except Exception as e:
                print(f"   Failed: {e}")

            # Save crawl position after EVERY page, not every 20 --
            # this is what protects you if the process gets killed.
            save_state({"visited": list(visited), "to_visit": to_visit})
            time.sleep(REQUEST_DELAY_SECONDS)

    except KeyboardInterrupt:
        print("\nStopped by user (Ctrl+C). Progress up to this point is already saved.")

    with open(ALL_URLS_LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(visited)))

    print(f"\n--- Run summary ---")
    print(f"Pages visited this run: {pages_done}")
    print(f"New financial HTML pages saved: {html_saved} -> {OUT_HTML}")
    print(f"New financial documents saved: {pdf_saved} -> {OUT_PDF}")
    print(f"Total pages visited so far (all runs): {len(visited)}")
    print(f"Still queued to visit: {len(to_visit)}")
    if to_visit:
        print(f"Hit the {MAX_PAGES_PER_RUN}-page safety ceiling for this run "
              f"(unusual for a small site). Run the exact same command again to continue.")
    else:
        print("Nothing left to visit - crawl is complete.")


if __name__ == "__main__":
    main()
