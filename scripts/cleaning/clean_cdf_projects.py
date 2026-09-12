import os
import pandas as pd


def clean_cdf_data():
    raw_path = "data/raw/cdf_projects/raw_cdf_projects.csv"
    processed_dir = "data/processed"
    processed_path = os.path.join(processed_dir, "db-unza26-csc4792-kalomo_town_council_cdf_projects.csv")

    if not os.path.exists(raw_path):
        print(f"Error: Could not find raw file at {raw_path}")
        return

    # Loading raw scraped data
    df = pd.read_csv(raw_path)

    # Renaming columns to standardized names expected downstream
    df = df.rename(columns={
        "title": "project_name",
        "snippet": "description",
        "link": "source_url"
    })

    # Dropping missing or invalid project names
    df = df.dropna(subset=["project_name"])
    df = df[df["project_name"] != "N/A"]

    # Stripping whitespace
    df["project_name"] = df["project_name"].astype(str).str.strip()
    df["description"] = df["description"].astype(str).str.strip()

    # Dropping duplicate projects
    df = df.drop_duplicates(subset=["project_name"])

    # Removing "...Continue reading" and the duplicated title
    df['description'] = df['description'].str.replace(r'\.\.\.Continue reading.*', '', regex=True)

    # Ensuring output directory exists and saving cleaned dataset
    os.makedirs(processed_dir, exist_ok=True)
    df.to_csv(processed_path, index=False, sep='|')
    
    print(f"Successfully cleaned data. Saved {len(df)} records to {processed_path}")

if __name__ == "__main__":
    clean_cdf_data()