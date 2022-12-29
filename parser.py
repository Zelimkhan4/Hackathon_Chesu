import requests
from PIL import Image
from io import BytesIO


base = "https://static-maps.yandex.ru/1.x/?"
args = ["l=map", "ll=37.620070,55.753630", "z=5"]
res = requests.get(base + "&".join(args))


Image = Image.open(BytesIO(res.content))
Image.save("static/images/image.png")
