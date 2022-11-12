#!/usr/bin/env python

from bs4 import BeautifulSoup
from time import sleep
import csv
import random
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 44.0.2403.157 Safari / 537.36",
    "Accept-Language": "en-US, en;q=0.5",
}


def main():
    with open("purchases.csv", "r") as infile, open("price_drops.txt", "w") as outfile:
        items = csv.DictReader(infile)
        item_list = []
        for item in items:
            item_list.append(item)

        outfile.write("url,cost,current_price,date,desc\n")

        for item in item_list:
            date = item["Order Date"]
            desc = item["Title"]
            asin = item["ASIN/ISBN"]
            cost = float(
                item["Purchase Price Per Unit"].replace("$", "").replace(",", "")
            )
            url = "https://www.amazon.com/dp/" + asin
            page = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(page.content, "lxml")

            price = float(
                soup.find("span", attrs={"class": "a-offscreen"})
                .string.strip()
                .replace("$", "")
                .replace(",", "")
            )

            if price < cost:
                outfile.write(f"{url},{cost:.2f},{price:.2f},{date},{desc}\n")
                print(f"{url},{cost:.2f},{price:.2f},{date},{desc}")

            sleep(random.randint(1, 10))


if __name__ == "__main__":
    main()
