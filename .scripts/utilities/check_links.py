#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_links(url):
    """Find all links on a given webpage."""
    try:
        page = requests.get(url)
        page.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(page.text, 'html.parser')
        return [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)]
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def check_link_status(link):
    """Check the status code of a given link."""
    try:
        response = requests.head(link, allow_redirects=True)
        if response.status_code != 200:
            print(f"{response.status_code}\t{link}")
    except requests.RequestException as e:
        print(f"Error checking {link}: {e}")

def main():
    url = input("Enter a web URL: ")
    links = find_links(url)
    for link in links:
        check_link_status(link)

if __name__ == "__main__":
    main()
