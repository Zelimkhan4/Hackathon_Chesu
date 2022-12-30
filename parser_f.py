import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from data import db_session
import json


def get_coords_from_address():
    coord_list = []

    base_url = "http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": "d0994865-bed2-439d-a391-b70eab2cabeb",
        "geocode": "sdfsfdfsf",
        "format": "json",
        "encoding": "UTF - 8"
     }
    req = requests.get(base_url, params=params)
    json_response = req.json()
    print(json_response["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"])
    if json_response["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"] != "0":

        with open("res.json", "w", encoding="UTF-8") as f:
            a = json.dump(json_response, f, indent=4)

        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coordinates = toponym["Point"]["pos"]
        print(toponym_coordinates)


get_coords_from_address()


def parse_hospitals(area):
    i = 1
    names = []
    res = requests.get(f"https://clinics.medsovet.info/{area}/bolnicy?page={i}")
    soup = BeautifulSoup(res.text, features="lxml")
    while len(soup.findAll("a", class_="clinic-item_name")):
        soup = BeautifulSoup(res.text, features="lxml")
        for elem in soup.findAll("a", class_="clinic-item_name"):
            names.append([elem.href, elem.text])
        i += 1
        res = requests.get(f"https://clinics.medsovet.info/{area}/bolnicy?page={i}")

    return names


def parse_news():
    parsed_data = []
    res = requests.get("https://chechnyatoday.com/content").text
    soup = BeautifulSoup(res, features="lxml")
    for div in soup.findAll("div", class_="row archive-item"):
        desc = div.find("a").text.strip()
        image_link = div.find("img")["src"].strip()
        parsed_data.append([desc, image_link])
    return parsed_data
