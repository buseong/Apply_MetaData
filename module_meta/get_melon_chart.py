import urllib
from random import randint
from urllib import request

from bs4 import BeautifulSoup

from Data import *

arr_work: list = []


def get_soup(url: str, usage: str):
    """
    get soup through bs4
    :param usage: usage
    :param url: get soup for url
    :return: Soup
    """
    opener = urllib.request.build_opener()
    header = headers[randint(0, len(headers) - 1)]
    opener.addheaders = header
    request.install_opener(opener)
    html = request.urlopen(url)
    Soup = BeautifulSoup(html.read(), "html.parser")
    print(f"{usage} : {url}")
    html.close()
    return Soup


def get_melon():
    soup = get_soup('https://www.melon.com/chart/index.htm', 'chart')
    top = 50  # 50) 50개 100) 50개 -> len-2
    id_list = [i['data-song-no'] for i in soup.select(f'.lst{top}')]
    print(id_list)
    return id_list


def get_title_artist(music_id):
    url = "https://www.melon.com/song/detail.htm?songId=" + str(music_id)
    soup = get_soup(url, 'get_tag')
    title = soup.select('.song_name')[0].get_text().replace('곡명', '').strip()
    artist = soup.select('.artist_name')[0].get_text()
    return title, artist, music_id


def get_chart(num: int):
    title, artist, music_id = get_title_artist(get_melon()[num])
    return title, artist, music_id

