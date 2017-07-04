#from redditWallpaper import html as html_doc
from ignorpasswd import passwd, modhash
import json
import urllib
import requests
from bs4 import BeautifulSoup
from subprocess import call

def conection(url):
    body = {
        'username': "neiho",
        'passwd': passwd
        }
    headers = {
        'x-modhash': modhash,
        'cache-control': "no-cache",
        'postman-token': "0802df05-b56d-a7b3-8c44-bee2a6e2a14e"
        }

    return requests.request("GET", url, headers=headers)

def soupolait(html_doc):
    soup = BeautifulSoup(html_doc.text, 'html.parser') #enlever .text si en test
    tabImg = soup.select(".thing")
    print (soup)

    i=0
    for a in tabImg[0].find_all('a', href=True):

        dictUrl[i] = ( a['href'])
        i+=1

    print (dictUrl[0])
    return dictUrl[0]


dictUrl={}
url = "https://www.reddit.com/r/wallpapers/hot"


urlImg=soupolait(conection(url))


# print (tabImg[0].find_all('a', href=True))


urllib.request.urlretrieve(urlImg,"fond/fond.jpg") #enregistre le fond dans le dossier fond sous le nom fond. jpg
call(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", "'file:///home/antoine/Documents/Dev/python/redditWallpapers/fond/fond.jpg'"]) #change le fond d'ecran de l'ordi #gnome3
