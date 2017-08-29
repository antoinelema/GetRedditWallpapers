#!/usr/bin/python3
# from redditWallpaper import html as html_doc
from ignorpasswd import passwd, clientID,clientSecret
from datetime import datetime
import json
import os
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
    # print ("token : ",token)
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

    # print (dictUrl[0])
    return dictUrl[0]


def step2(url,token):
    """ ouvre le lien trouvé qui n'était pas sune image, si le lien renvoi sur reddit => rechercher l'image """
    print("nouvelle essai ...")
    if url.rfind("/r/wallpapers") > -1:
        recherche = ".media-preview-content"
        return(soupolait(Get("https://www.reddit.com{}".format(url),token),recherche))
    else :
        print ("echec ... fermeture ... ")
        sys.exit()


def checkUrlImg(urlImg,token):
    """ verifie que l'url est une image, si non envoi en step2 """
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

def ext(url):
    """ trouve et renvoi l'estention d'une url """
    filename, file_extension = os.path.splitext(url)
    return(file_extension)

def changefond(trueUrlImg):
    """ enregistre l'image et la met en fond """
    now=datetime.now()
    extension=ext(trueUrlImg)
    cheminCourrant = os.getcwd()
    cheminImg = "fond/fond.{}-{}-{}{}".format(now.day,now.month,now.year,extension)
    print("telechargement ...")
    urllib.request.urlretrieve(trueUrlImg, cheminImg)
    call(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "file://{}".format(cheminCourrant + '/' + cheminImg)])  # change le fond d'ecran de l'ordi #gnome3
    # cherhcer une alternative a fille/// sui ne permet pas les lien

token = getToken()
recherche = ".thing"
url = "https://www.reddit.com/r/wallpapers/hot"
urlImg = soupolait(Get(url,token),recherche)
trueUrlImg = checkUrlImg(urlImg,token)
changefond(trueUrlImg)

# print (tabImg[0].find_all('a', href=True))
