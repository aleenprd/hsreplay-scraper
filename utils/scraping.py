# %%
"""Methods related to scraping."""


# IMPORTING PACKAGES
# -------------------------------------- #
import pandas as pd
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, List
import numpy as np
from tqdm import tqdm
from time import sleep
import traceback
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from utils import miscelaneous as msc
from utils import scraping as scr


# %%
def make_soup(url: str, header: str) -> BeautifulSoup:
    """
    Return an HTML body from an URL.

    Obs: Soup is not enoug hfor this site.
    We need to interact with the JavaScript,
    so we will use Selenium with ChromeDriver.
    """
    # https://stackoverflow.com/questions/13303449/
    # urllib2-httperror-http-error-403-forbidden

    # https://stackoverflow.com/questions/
    # 40255128/how-to-parse-the-website-using-beautifulsoup

    # Changing the header was needed in this method
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.text, 'html.parser')

    return soup


def make_soup_with_selenium(
    url: str,
    chrome_driver_path: str
) -> BeautifulSoup:
    """
    Return an HTML body from an URL.

    Obs: Soup is not enoug hfor this site.
    We need to interact with the JavaScript,
    so we will use Selenium with ChromeDriver.
    """

    # https://stackoverflow.com/questions/13303449/
    # urllib2-httperror-http-error-403-forbidden

    # https://stackoverflow.com/questions/
    # 40255128/how-to-parse-the-website-using-beautifulsoup

    # Start-up Selenium
    driver = webdriver.Chrome(chrome_driver_path)
    driver.maximize_window()
    driver.get(url)
    sleep(5)

    # Get page source code
    page_source = driver.page_source

    # Make a BeautifulSoup
    soup = BeautifulSoup(page_source, 'lxml')

    return soup


def check_list_lens(li: List) -> bool:
    """Chekcs if all lists in a list have the same length."""
    # https://stackoverflow.com/questions/35791051/
    # better-way-to-check-if-all-lists-in-a-list-are-the-same-length

    return not any(len(li[0]) != len(i) for i in li)


def lol_to_df(
    lol: List,
    columns=["Deck", "Class", "Tier", "Winrate", "Archetype_URL"]
) -> pd.DataFrame:
    """Make Pandas DF from List of Lists."""
    # https://datascience.stackexchange.com/questions/
    # 26333/convert-a-list-of-lists-into-a-pandas-dataframe
    if len(lol) == len(columns):
        df = pd.DataFrame(lol, columns)
        return df
    else:
        print("\nERROR: Mismatch between number of features and column names.")

        return pd.DataFrame()


def scrape_meta_snapshot(url, chrome_driver_path):
    """Scrape the HsReplay meta snapshot main page."""
    # Get Beautiful Soup using Selenium
    # -------------------------------------- #
    soup = make_soup_with_selenium(url, chrome_driver_path)

    # Get deck names
    # -------------------------------------- #
    div_archetype_name = soup.find_all("div", {"class": "archetype-name"})

    decks = []
    for d in div_archetype_name:
        decks.append(d.text)

    # Get deck class
    # -------------------------------------- #
    classes = []
    for d in decks:
        temp = d.split(" ")
        classes.append(temp[-1])

    # Get number of decks per tier
    # -------------------------------------- #
    div_tier = soup.find_all("div", {"class": "tier"})

    decks_per_tier = []
    for t in div_tier:
        decks_per_tier.append(t.text.count("%"))

    # Get tier number for each deck
    # -------------------------------------- #
    tiers_ranks = [x for x in range(1, len(decks_per_tier)+1)]

    tier_list = []
    for i in range(0, max(tiers_ranks)):
        for j in range(decks_per_tier[i]):
            tier_list.append(f"Tier {i+1}")
    tier_list

    # Get deck winrates
    # -------------------------------------- #
    div_archetype_data = soup.find_all("div", {"class": "archetype-data"})

    winrates = []
    for w in div_archetype_data:
        winrates.append(float(w.text.replace("%", "")))

    # Get archetype link
    # -------------------------------------- #
    a_elements = soup.find_all("a", href=True)

    urls = []
    for a in a_elements:
        href = a['href']
        if '/archetypes/' in href:
            urls.append(href)

    # Check all lists have same length
    # -------------------------------------- #
    features = [
        decks,
        classes,
        tier_list,
        winrates,
        urls
    ]
    if check_list_lens(features) is not True:
        print("\nERROR: The lists of features have different lengths!\n")
    else:
        pass

    return features
