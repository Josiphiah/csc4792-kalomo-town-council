import os
import urllib3
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Suppressing SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def fetch_cdf_data():
    url = "https://www.kalomocouncil.gov.zm/?s=CDF"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    # Ignoring the unverified SSL certificate from the site
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    return response.text


def parse_cdf_projects(html):
    soup = BeautifulSoup(html, "html.parser")
    projects = []

    # Parsing search results / articles
    articles = soup.find_all("article")
    for article in articles:
        title_elem = article.find(["h2", "h3", "h1"])
        link_elem = article.find("a")
        snippet_elem = article.find(["p", "div", "entry-summary"])

        title = title_elem.get_text(strip=True) if title_elem else "N/A"
        link = link_elem["href"] if link_elem and "href" in link_elem.attrs else "N/A"
        snippet = snippet_elem.get_text(strip=True) if snippet_elem else "N/A"

        projects.append(
            {"title": title, "link": link, "snippet": snippet}
        )

    return projects


def save_raw_data(data):
    # Ensuring directory exists relative to project root
    os.makedirs("data/raw", exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv("data/raw/raw_cdf_projects.csv", index=False)
    print(f"Saved {len(df)} scraped records to data/raw/raw_cdf_projects.csv")


if __name__ == "__main__":
    try:
        print("Fetching CDF data from Kalomo Town Council website...")
        html_content = fetch_cdf_data()
        project_data = parse_cdf_projects(html_content)

        if project_data:
            save_raw_data(project_data)
            print("Scraping complete.")
        else:
            print("No project entries found on the target page.")
    except Exception as e:
        print(f"An error occurred during scraping: {e}")