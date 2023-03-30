import os
import requests
from lxml import html
from pathlib import Path
import sys

url = "https://www.smogon.com/stats/"
data_dir = os.path.join(os.getcwd(), "data")

def download_files(url, dir_path=data_dir):
    # use pathlib to create the directory whether the parent directory exists or not
    Path(dir_path).mkdir(parents=True, exist_ok=True)

    response = requests.get(url)
    parsed_body = html.fromstring(response.content)
   
    for index in range(1, 9999):
        try:
            link = parsed_body.xpath("/html/body/pre/a[{index}]".format(index=index))[0]
        except IndexError:
            break
        text = link.text
        if ".." in text:
            continue
        if "." in text:
            file_url = url + text
            file_path = os.path.join(dir_path, file_url.split("/")[-1])
            print("Downloading", file_url)
            r = requests.get(file_url)
            with open(file_path, "wb") as f:
                f.write(r.content)
            print("Downloaded", file_url)
        else:
            new_url = url + text
            new_dir = os.path.join(dir_path, text)
            download_files(new_url, new_dir)


def batch_download_by_year(YEAR):
    response = requests.get(url)
    parsed_body = html.fromstring(response.content)
    for index in range(1, 9999):
        try:
            link = parsed_body.xpath("/html/body/pre/a[{index}]".format(index=index))[0]
        except IndexError:
            break
        text = link.text
        if str(YEAR) in text:
            print("Downloading", YEAR)
            new_url = url + text
            new_dir = os.path.join(data_dir, str(YEAR), text)
            download_files(new_url, new_dir)


    year_url = url + str(YEAR) + "/"
    year_dir = os.path.join(data_dir, str(YEAR))
    download_files(year_url, year_dir)

def _test_parse():
    response = requests.get(url)
    parsed_body = html.fromstring(response.content)
    link = parsed_body.xpath("/html/body/pre/a[999]")[0]
    #text = link.text
    #print(text)

if __name__ == "__main__":
    batch_download_by_year(2023)