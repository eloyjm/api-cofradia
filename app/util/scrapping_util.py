# encoding:utf-8

from bs4 import BeautifulSoup
import urllib.request
import re
import os
import ssl

if not os.environ.get("PYTHONTTPSVERIFY", "") and getattr(
    ssl, "_create_unverified_context", None
):
    ssl._create_default_https_context = ssl._create_unverified_context


def extract_data_wiki(url: str):

    data = {}
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")
    pattern = r"\[\d+\]|\u200b"

    table = s.find("table", class_="infobox")
    for row in table.find_all("tr"):
        if row.find("th") and row.find("td"):
            key = row.find("th").text.replace("\xa0", " ").strip()
            value = (
                row.find("td")
                .text.replace("\xa0", " ")
                .replace("\n", " ")
                .strip()
            )
            value = re.sub(pattern, "", value)
            if key not in data:
                data[key] = value

    keys = [
        "Descripcción",
        "Localidad",
        "Sede canónica",
        "Fundación",
        "Titulares",
        "Pasos",
        "Hermanos",
        "Nazarenos",
        "Día y hora",
        "Túnica",
        "Historia",
    ]

    description = []
    s_post_table = table.find_next_sibling()
    p1 = s_post_table
    while p1 and p1.name != "h2":
        if p1.name == "p" and p1.text:
            p1_text = re.sub(pattern, "", p1.text)
            description.append(p1_text.strip())
        p1 = p1.find_next_sibling()
    data["Descripcción"] = " ".join(description)

    title_h2 = s.find_all("h2")

    for h2 in title_h2:
        key = h2.text.replace("[editar]", "").strip()

        values = []

        p1 = h2.find_next_sibling()

        while p1 and p1.name != "h2":
            if p1.name == "p" and p1.text:
                p1_text = re.sub(pattern, "", p1.text)
                values.append(p1_text.strip())

            p1 = p1.find_next_sibling()
        data[key] = " ".join(values)

    result = {key: data.get(key, "No disponible") for key in keys}
    return result


def extract_data_dds(url: str):
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")

    table = s.find("table", class_="movil")
    data = []
    rows = table.find_all("tr")
    for i, row in enumerate(rows):
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        if i == 0:
            continue
        if cols[1]:
            data.append(("CRUZ", cols[0], cols[1]))
        if cols[2]:
            data.append(("PALIO", cols[0], cols[2]))

    map = s.find("div", class_="mapa")
    map_src = map.find("iframe")
    if map_src:
        map_src = map_src.get("src")

    return data, map_src


def extract_data_marcha(url: str):
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")
    res = list()
    rows = s.find_all("h3")
    for row in rows:
        data = {}
        text = row.text.split("(")
        if len(text) > 1:
            data["name"] = text[0].split(".")[1].strip()
            data["author"] = text[1].split(")")[0]
            data["url"] = row.find("a").get("href")
            p = row.find_next_sibling("p")
            data["description"] = ""
            if p:
                data["description"] = p.text
            res.append(data)
    return res
