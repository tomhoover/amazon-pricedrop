#!/usr/bin/env python

from bs4 import BeautifulSoup
from time import sleep
import csv
import random
import requests
import os
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36",
    "Accept-Language": "en-US, en;q=0.5",
}


def main():
    # fmt:off
    with open("purchases.csv", "r") as infile, open("price_drops.txt", "w") as outfile, open("all.txt", "w") as allfile:
    # fmt:off
        items = csv.DictReader(infile)
        item_list = []
        for item in items:
            item_list.append(item)

        allfile.write("url,cost,current_price,date,desc\n")
        outfile.write("url,cost,current_price,date,desc\n")

        for item in item_list:
            date = item["Order Date"]
            desc = item["Title"]
            asin = item["ASIN/ISBN"]
            cost = float(
                item["Purchase Price Per Unit"].replace("$", "").replace(",", "")
            )
            url = "https://www.amazon.com/dp/" + asin

            if os.isatty(sys.stdout.fileno()):
                print(f"  * Downloading {desc}")

            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, "lxml")

            if desc == "":
                desc = soup.find(id="productTitle").get_text().strip()
                # print(desc)

            price = ""
            try:
                price = float(
                    soup.find("span", attrs={"class": "a-offscreen"})
                    .string.strip()
                    .replace("$", "")
                    .replace(",", "")
                )
            except ValueError as err:
                print(f"ValueError: {err}")
                price = 0
            except AttributeError:
                price = "N/A"

            allfile.write(f"{url},{cost:.2f},{price},{date},{desc}\n")

            if type(price) == str or price < cost:
                outfile.write(f"{url}\t{cost:.2f}\t{price}\t{date}\t{desc}\n")
                if os.isatty(sys.stdout.fileno()):
                    print(f"{url}, {cost}, {price}, {date}, {desc}")

            sleep(random.randint(1, 10))


if __name__ == "__main__":
    main()
