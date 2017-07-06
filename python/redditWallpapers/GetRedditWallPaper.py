# from redditWallpaper import html as html_doc
from ignorpasswd import passwd, modhash, clientID,clientSecret
from datetime import datetime
import json
import sys
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
        'User-Agent': 'My User Agent GetRedditWallpaper',
        'From': 'neiho'
        }

    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
    json_data = response.json()
    token = json_data['access_token']
    print ("token : ",token)
    return token

def Get(url,token):
    """Conection et Get du site."""
    querystring = {
        "access_token" : token
        }
    headers = {
        'User-Agent': 'My User Agent GetRedditWallpaper',
        'From': 'neiho'
        }

    return requests.request("GET", url, headers=headers, params=querystring)


def soupolait(html_doc,recherche):
    """
    Transforme du html en str avec BeautifulSoup.
    Trouve le lien de l'image recherché.
    """
    dictUrl = {}
    soup = BeautifulSoup(html_doc.text, 'html.parser')  # enlever .text si en test
    tabImg = soup.select(recherche)  # ne retient que les element de la recherche
    print ("make some soup")

    i = 0
    for a in tabImg[0].find_all('a', href=True):

        dictUrl[i] = (a['href'])
        i += 1

    print (dictUrl[0])
    return dictUrl[0]


def step2(url,token):
    if url.rfind("i.redd.it") > -1:
        recherche = ".media-preview-content"
        soupolait(Get(url,token),recherche)
    else :
        print ("echec ... fermeture ... ")
        sys.exit()


def checkUrlImg(urlImg,token):
    listext = ["jpg","jpeg","png","bmp"]
    # extention d'image
    urlImgMin = urlImg.lower()  # metre url en minuscule
    for ext in listext:
        if urlImgMin.rfind(ext) > -1:
            print("image trouvée")
            return urlImg
    else:
        print ("image non trouée ...")
        return step2(urlImg,token)


def changefond(trueUrlImg):
    now=datetime.now()
    print("telechargement ...")
    urllib.request.urlretrieve(urlImg, "fond/fond.{}-{}-{}.{}".format(now.day,now.month,now.year,ext))
    # {}".format(urlImg))  # enregistre le fond dans le dossier fond sous le nom fond.jpg
    call(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "'file:///home/antoine/Documents/Dev/python/redditWallpapers/fond/fond.jpg'"])  # change le fond d'ecran de l'ordi #gnome3

token = getToken()
recherche = ".thing"
url = "https://www.reddit.com/r/wallpapers/hot"
urlImg = soupolait(Get(url,token),recherche)
trueUrlImg = checkUrlImg(urlImg,token)
changefond(trueUrlImg)

# print (tabImg[0].find_all('a', href=True))
