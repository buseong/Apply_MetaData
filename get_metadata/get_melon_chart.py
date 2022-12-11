import urllib
from random import randint
from urllib import request
from utill.utill import check_type, pprint
from bs4 import BeautifulSoup

from Data import *

arr_work: list = []


def get_soup(url: str, usage: str):
    """
    get soup
    :param url: to get soup
    :param usage: to record where this function was executed
    :return: soup
    """
    check_type(url, str)
    check_type(usage, str)

    pprint(f'{usage} : {url}')
    opener = request.build_opener()
    header = headers[randint(0, len(headers) - 1)]
    opener.addheaders = header
    request.install_opener(opener)
    with request.urlopen(url) as html:
        soup = BeautifulSoup(html.read(), "html.parser")
    return soup


def get_melon():
    soup = get_soup('https://www.melon.com/chart/index.htm', 'chart')
    top = 50  # 50 -> top-50, 100 -> top-50 + top-100(len=50)
    id_list = [i['data-song-no'] for i in soup.select(f'.lst{top}')]
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

