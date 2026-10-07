#!/usr/bin/env python3
"""Fetch the Pets: collect the dog pages and the pets on a page.

The Trailside Animal Shelter lists its dogs across 6 pages and its cats
across 4. Before a later assignment can visit every pet, you need the full
URL of each dog page, and the full URL of each pet on a page.
"""

import re

import requests
from bs4 import BeautifulSoup

# Toolkit (from class): don't change
BASE = "https://moden-coding.github.io/scrape-practice-site/shelter/"


def fetch_and_save(url, path):
    resp = requests.get(url, timeout=20)
    resp.encoding = "utf-8"
    with open(path, "w", encoding="utf-8") as f:
        f.write(resp.text)
    return resp.status_code


def load_soup(path):
    with open(path, encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


# Your code below


def dog_page_urls(soup):
    """Return a list of the full URLs of all 6 dog pages, with no duplicates and no cat pages."""
    pass


def pet_urls(soup):
    """Return a list of the full URLs of the pet detail pages on this page, with no duplicates."""
    pass


def main():
    status = fetch_and_save(BASE + "dogs-page-1.html", "dogs-page-1.html")
    print("Status:", status)
    soup = load_soup("dogs-page-1.html")

    pages = dog_page_urls(soup)
    pets = pet_urls(soup)
    print("Found", len(pages), "dog page URLs")
    print(pages[:3])
    print("Found", len(pets), "pet URLs")
    print(pets[:3])


if __name__ == "__main__":
    main()
