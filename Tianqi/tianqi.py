import requests
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

def grab_tianqia(city, year, month):
    url = f"https://lishi.tianqi.com/{city}/{year}{month:02}.html"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.63"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content)
    ul = soup.find('ul', attrs={"class": "thrui"})
    data = [i.text.strip().split() for i in ul.find_all('li')]
    return data


if __name__ == '__main__':
    output_file = "tianqi.csv"
    city = "haining"
    with open(output_file, "a") as f:
        for year in range(2021, 2022):
            for month in range(1, 4):
                print(f"grabing {year} - {month:02}")
                data = grab_tianqia(city, year, month)
                for i in range(len(data)):
                    f.write(",".join(data[i]))
                    f.write("\n")
                sleep(0.1)
