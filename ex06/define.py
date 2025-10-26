import sys
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Expected exactly one argument")
        exit(-1)

    page = requests.get(f"https://www.britannica.com/dictionary/{quote_plus(sys.argv[1])}")
    b = BeautifulSoup(page.content, features="html.parser")
    i = 1
    for d in b.find_all("span", {"class": "def_text"}):
        print(f"Def #{i}: {d.text}")
        i += 1
