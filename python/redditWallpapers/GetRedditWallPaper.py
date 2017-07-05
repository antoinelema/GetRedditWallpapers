# from redditWallpaper import html as html_doc
from ignorpasswd import passwd, modhash, clientID,clientSecret

import json
import urllib
import requests
import requests.auth
from bs4 import BeautifulSoup
from subprocess import call

def getToken():
    client_auth = requests.auth.HTTPBasicAuth(clientID, clientSecret)
    post_data = {
        "grant_type": "password",
        "username": "neiho",
        "password": passwd
        }
    headers = {
        "User-Agent": "neiho"
        }

    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    json_data = response.json()
    token = json_data['access_token']
    return token

def conection(url):
    """Conection et Get du site."""
    querystring = {"access_token":getToken}
    headers = {
        'x-modhash': modhash
        }

    return requests.request("GET", url, headers=headers, params=querystring)


def soupolait(html_doc):
    """
    Transforme du html en str avec BeautifulSoup.
    Trouve le lien de l'image recherché.
    """
    dictUrl = {}
    soup = BeautifulSoup(html_doc.text, 'html.parser')  # enlever .text si en test
    tabImg = soup.select(".thing")  # ne retient que les element de la class thing
    # print (soup)

    i = 0
    for a in tabImg[0].find_all('a', href=True):

        dictUrl[i] = (a['href'])
        i += 1

    print (dictUrl[0])
    return dictUrl[0]


def step2(urlImg):
    # trouver nature url et refaire un get
    pass


def checkUrlImg(urlImg):
    ext1 = "jpg"
    ext2 = "jpeg"
    ext3 = "png"
    ext4 = "bmp"  # extention d'image
    urlImgMin = urlImg.lower()  # metre url en minuscule
    if urlImgMin.rfind(ext1) > -1 or urlImgMin.rfind(ext2) > -1 or urlImgMin.rfind(ext3) > -1 or urlImgMin.rfind(ext4) > -1:
        print("image trouvé"")
        return urlImg
    else:
        return step2(urlImg)


def changefond(trueUrlImg):
    urllib.request.urlretrieve(urlImg, "fond/fond.jpg")  # enregistre le fond dans le dossier fond sous le nom fond.jpg
    call(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "'file:///home/antoine/Documents/Dev/python/redditWallpapers/fond/fond.jpg'"])  # change le fond d'ecran de l'ordi #gnome3


url = "https://www.reddit.com/r/wallpapers/hot"
urlImg = soupolait(conection(url))
trueUrlImg = checkUrlImg(urlImg)
changefond(trueUrlImg)

# print (tabImg[0].find_all('a', href=True))
