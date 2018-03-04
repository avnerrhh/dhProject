import urllib
import re
import codecs
from os import walk

import swagger_client
from googleapiclient.errors import HttpError
from lxml import html
from lxml import etree
from lyrics_api import get_row_data, get_lyric_from_data, youtube_addres
from youtube_comments import get_comments_from_youtube_code, get_youtube_id

import re
from six.moves import urllib

from bs4 import BeautifulSoup


def get_lyrics(artist, song_title):
    artist = artist.lower()
    song_title = song_title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    if artist.startswith("the"):  # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/" + artist + "/" + song_title + ".html"

    try:
        # need to add apikey from MusicMatch for it to work
        #swagger_client.configuration.api_key['apikey'] = here is the place where yours key goes
        # create an instance of the API class
        #content = swagger_client.TrackApi().api_client.request('GET', url).data
        #if there isn't a key, this line works but get blocked if used to many times.
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>', '').replace('</br>', '').replace('</div>', '').strip()
        return lyrics
    except Exception as e:
        return "Exception occurred \n" + str(e)

# def equal_name(text, name):
#     words = text.lower().replace(" ","").replace(".","").replace(",","")
#     name_words = name.lower().replace(" ","").replace(".","").replace(",","")
#     return words == name_words
#
#
#
def get_lyrics_and_youtube_comments(artist,song_name):
     ans = []
     ans.append(get_lyrics(artist,song_name).replace("<br/>", ""))
     ans.append(get_youtube_id(song_name))

     return ans
#
#
#
# def get_lyrics(name):
#     name_to_url = name.split()
#     url = "https://www.lyrics.com/lyrics/"
#     for i in range(0,len(name_to_url) - 1):
#         url += name_to_url[i] + "%20"
#     url += name_to_url[len(name_to_url) - 1]
#     page = html.fromstring(urllib.urlopen(url).read())
#     flag = False
#     ans = [None,None]
#     i = 0
#     for link in page.xpath("//a"):
#         if flag and link.text != None:
#             ans = get_lyrics_youtube_from_url(link.get("href"))
#             print link.get("href")
#
#         if link.text != None and len(link.text) > 2 and link.text[:3] == "and":
#             flag = True
#         if link.text != None and len(link.text) > 0 and (link.text[:1] == "1"):
#             flag = False
#     return ans
#
# def offline_mode():
#     path = "C:\\Users\\Avner\\PycharmProjects\\dhProject\\songs_lists"
#     i = 0
#     for (dir_path, dir_names, file_names) in walk(path):
#         for i in range(0, len(file_names)):
#             with codecs.open(dir_path + '\\' + file_names[i], 'r', 'utf8') as f:
#                 if("songs_list.txt" == file_names[i]):
#                     for content in f:
#                         song_info = get_lyrics(content.replace("\n", "").replace("\r",""))
#                         if (song_info[0] != None):
#                             lyrics_file = open(dir_path+"\\lyrics_"+str(i)+".txt",'w')
#                             lyrics_file.write(song_info[0])
#                             lyrics_file.close()
#                         print song_info[1]
#                         if (song_info[1] != None):
#                             comments_file = open(dir_path+'\\comments_'+str(i)+'.txt','w')
#                             for comment in song_info[1]:
#                                 comment = comment.replace(u'\xfc',"")
#                                 comments_file.write("%s\n" % comment)
#                                 comments_file.write("\n")
#                             comments_file.close()
#                         i+=1
#
# get_lyrics("on a dark desert highway")
# #print get_lyrics("American Woman")
#offline_mode()

#print get_lyrics_and_youtube_comments("perfect","Ed Sheeran")[1]
# print get_lyrics_and_youtube_comments("Hotel California" ,"Eagles ")[1]
# print get_lyrics_and_youtube_comments("led zeppelin" ,"kashmir")[1]