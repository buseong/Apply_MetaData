import random
import re
import time
import urllib
import urllib.request

from bs4 import BeautifulSoup

from module_meta.Data import *


def get_soup(url: str, usage: str):
    """
    get soup through bs4
    :param usage: usage
    :param url: get soup for url
    :return: Soup
    """
    opener = urllib.request.build_opener()
    rand_ = random.randint(0, len(headers) - 1)
    header = headers[rand_]
    opener.addheaders = header
    urllib.request.install_opener(opener)
    html = urllib.request.urlopen(url)
    Soup = BeautifulSoup(html.read(), "html.parser")
    print(f"{usage} {html.status}: {url}")
    html.close()
    return Soup


def get_music_id(title: str, artist: str = '') -> str or int:
    """
    Get music in melon
    :param title: str, title of mpeg-3 file
    :param artist: str, artist of mpeg-3 file
    # :param search_number: int, not recommend change
    :return: album title, album artist, album id in melon
    """
    if artist != '':
        url = "https://www.melon.com/search/song/index.htm?q=" + urllib.parse.quote(title) \
              + '+' + urllib.parse.quote(artist)
        print(f"{title} + {artist} : {url}")
    else:
        url = "https://www.melon.com/search/song/index.htm?q=" + urllib.parse.quote(title)
        print(f"{title} : {url}")
    soup = get_soup(url, 'get_melon_info')
    music_id_list = [int(re.findall('\'(.+?)\'', str(re.findall(r'searchLog\((.+?)\);', k['href'])[0]).split(',')[music_id_l])[0]) for k in soup.select(".fc_gray")]
    album_list = [soup.select('.fc_mgray')[i].get_text() for i in range(len(soup.select(".fc_mgray"))) if i % 3 == 2]
    title_list = [str(j['title']).rstrip(' - 페이지 이동') for j in soup.select(".fc_gray")]
    # print(title_list)
    # print(music_id_list)
    print(album_list)
    if title in album_list:
        music_id = music_id_list[title_list.index(title)]
    else:
        music_id = music_id_list[0]
    print(music_id)
    print(type(music_id))
    return music_id


if __name__ == '__main__':
    start_time = time.time()
    music_id = get_music_id('After Like', 'ive')
    print(music_id)
    url = "https://www.melon.com/song/detail.htm?songId=" + str(music_id)
    print(url)
    print(time.time() - start_time)
