import xml.etree.ElementTree as ET
import html
import swagger_client
import RestResponse
import json
from swagger_client.rest import ApiException

# str | Account api key, to be used in every api call

def get_row_data(url):
    swagger_client.configuration.api_key['apikey'] = 'bc0dfae0b57b1305f3a3daf05cb4ea20'
    # create an instance of the API class
    api_instance = swagger_client.TrackApi().api_client.request('GET',url)
    return api_instance.data


def clean(data):
    ans = ""
    i = 0
    while i < len(data):
        if data[i] == '<':
            j = 0
            while data[i + j] != '>':
                j += 1
            i += j + 1
        ans += data[i]
        i += 1
    return ans


def get_lyric_from_data(data):
    for i in range(0, len(data)):
        if (i + 16 < len(data) and data[i] == '<' and data[i + 1] == 'p' and data[i + 2] == 'r' and data[
            i + 3] == 'e' and
                data[i + 4] == ' ' and data[i + 5] == 'i' and data[i + 6] == 'd'):
            j = 0
            while data[i + j] != '>':
                j += 1
            k = j
            flag = 0
            while flag != 0 or (
                    data[i + k] != '<' or data[i + k + 1] != '/' or data[i + k + 2] != 'p' or data[i + k + 3] != 'r' or
                    data[i + k + 4] != 'e' or data[i + k + 5] != '>'):
                if (data[i + k] == '<' and data[i + k + 1] == 'p' and data[i + k + 2] == 'r' and data[
                    i + k + 3] == 'e' and data[i + k + 4] == '>'):
                    flag += 1
                if flag > 0 and (data[i + k] == '<' and data[i + k + 1] == '/' and data[i + k + 2] == 'p' and data[
                    i + k + 3] == 'r' and data[i + k + 4] == 'e'
                                 and data[i + k + 5] == '>'):
                    flag -= 1
                k += 1
            str = data[i + j + 1:]
            return clean(str[:k - j - 1])


def youtube_addres(data):
    for i in range(0, len(data)):
        if (i + 27 < len(data) and data[i:][:27] == '<div class="youtube-player"' ):
            return data[i+37:][:11]
