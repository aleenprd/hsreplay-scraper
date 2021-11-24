"""Scrape HsReplay Meta website for all meta decks info."""


# IMPORTING PACKAGES
# -------------------------------------- #
import pandas as pd
import os
from time import time
from utils import miscelaneous as msc
from utils import scraping as scr


# MAIN METHOD
# -------------------------------------- #
if __name__ == "__main__":
    # Keep track of runtime
    runtime_start = time()
    print("\nCommencing Hearthstone Meta scraper...")

    # Unpack the configuration options
    # -------------------------------------- #
    config_path = "config/meta_scraper_config.json"
    config_options = msc.load_configuration_file(config_path)
    header, url, chrome_driver_path, \
        output_path = msc.unpack_meta_scraper_config(config_options)

    # Scrape main page for URL list to parse
    # -------------------------------------- #
    print("\nExtracting archetype info...")
    features = scr.scrape_meta_snapshot(url, chrome_driver_path)

    # Make a dataframe
    print("\nForming DataFrame...")
    df = pd.DataFrame.from_records(features)
    df = df.T
    columns = [
        "Deck",
        "Class",
        "Tier",
        "Winrate",
        "Archetype_URL"
    ]
    df.columns = columns
    df = df.dropna()

    # Saving the data to disk
    if not os.path.exists("data/meta"):
        os.makedirs("data/meta")

    df.to_csv(output_path, index=False)

    # Keeping track of runtime.
    runtime_end = time()
    print(f"\nFinished in {round(runtime_end-runtime_start,2):,}s...")
