#!/usr/bin/python

# Usage:
# python scraper.py --videoid='<video_id>'
import argparse
from argparse import ArgumentError

from apiclient.errors import HttpError
from oauth2client.tools import argparser
from apiclient.discovery import build


YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEVELOPER_KEY = 'AIzaSyALIaMwCTin1BCBJJRoq5p3LwZsK7n2t0s'


# Sample python code for search.list


def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.iteritems():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def search_list_by_keyword(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.search().list(
    **kwargs
  ).execute()

  return response




def get_comment_threads(youtube, video_id, comments):
   threads = []
   results = youtube.commentThreads().list(part="snippet",maxResults=100,videoId=video_id,textFormat="plainText").execute()
   for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        comments.append(text)
   return comments


def get_comments(youtube, parent_id, comments):
  results = youtube.comments().list(
    part="snippet",
    maxResults=100,
    parentId=parent_id,
    textFormat="plainText"
  ).execute()

  for item in results["items"]:
    text = item["snippet"]["textDisplay"]
    comments.append(text)

  return results["items"]

def get_comments_from_youtube_code(youtube_id):
    try:
        argparser.add_argument("--videoid", help="Required; ID for video for which the comment will be inserted.")
        args = argparser.parse_args()
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        try:
            comments = []
            video_comment_threads = get_comment_threads(youtube, youtube_id, comments)
            return video_comment_threads
        except HttpError, e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    except ArgumentError, e:
        flag = True

def get_youtube_id(song_name):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    x = search_list_by_keyword(youtube,
        part='snippet',
        maxResults=25,
        q=song_name,
        type='')
    comments = []
    return get_comment_threads(youtube, x['items'][0]['id']['videoId'], comments)
