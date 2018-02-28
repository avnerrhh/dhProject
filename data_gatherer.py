import urllib
import re
from lxml import html
from lxml import etree

from lyrics_api import get_row_data, get_lyric_from_data, youtube_addres


def equal_name(text, name):
    words = text.lower().replace(" ","").replace(".","").replace(",","")
    name_words = name.lower().replace(" ","").replace(".","").replace(",","")
    return words == name_words


def get_song_commets(param):
    pass


def get_lyrics_youtube_from_url(parm):
    url = "https://www.lyrics.com"
    url += parm
    print url
    data = get_row_data(url)
    ans = []
    ans.append(get_lyric_from_data(data))
    print ans[0]
    youtube_code = youtube_addres(data)
    
    return ans



def get_lyrics(name):
    name_to_url = name.split()
    url = "https://www.lyrics.com/lyrics/"
    for i in range(0,len(name_to_url) - 1):
        url += name_to_url[i] + "%20"
    url += name_to_url[len(name_to_url) - 1]
    page = html.fromstring(urllib.urlopen(url).read())
    flag = False
    i = 0
    for link in page.xpath("//a"):
        if flag and link.text != None:
            if (equal_name(link.text, name)):

                 return get_lyrics_youtube_from_url(link.get("href"))
        if link.text != None and len(link.text) > 2 and link.text[:3] == "and":
            flag = True
        if link.text != None and len(link.text) > 0 and (link.text[:1] == "1"):
            flag = False
    return "Not Found"

get_lyrics("la woman")