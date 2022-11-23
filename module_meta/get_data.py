"""
Made By Buseong
"""
import re
from random import randint
from urllib import request
from urllib.parse import quote

import eyed3
from bs4 import BeautifulSoup
from googletrans import Translator

from .Data import *

not_work_list = []


def get_soup(url: str, usage: str, log: bool):
    """
    get soup
    :param url: to get soup
    :param usage: to record where this function was executed
    :param log: log console-print
    :return: soup
    """
    pprint(f"{usage} : {url}", log=log)
    opener = request.build_opener()
    header = headers[randint(0, len(headers) - 1)]
    opener.addheaders = header
    request.install_opener(opener)
    with request.urlopen(url) as html:
        soup = BeautifulSoup(html.read(), "html.parser")
    return soup


def pprint(text, log: bool = False):
    """
    print text-instance but types-instance is False: Not print
    :param text: to print text
    :param log: True or False
    """
    if log:
        print(text)
    else:
        pass


def remove_text(text: str):
    """
    remove text in text-instance
    :param text: to remove text
    :return: text
    """
    text_r = ''
    for i in expect_title:
        if i in text:
            text_r = text.replace(i, '')
            text = text_r
        else:
            text_r = text
    return text_r


def not_working_list(target: str = ...):
    """
    if target-instance is None, return "not_work_list": list
    if target-instance is not None, append target-instance to not_work_list
    :param target: file not running explorer address
    :return: not_work_list
    """
    if target is ...:
        return not_work_list
    not_work_list.append(str(target))
    return None


def tran_text(text: str, spilt_t: str = '+') -> str:
    """
    translation text
    :param text: to translation text
    :param spilt_t:
    :return:
    """
    if spilt_t in text:
        result = ' + '.join(tran_text(remove_text(i).strip()) for i in spilt_text(text, spilt_t))
    else:
        result = str(Translator().translate(text, src='en', dest='ko').text).strip()
    return result


def get_img_by_url(url: str) -> bytes:
    """
    get img by url_img-instance
    :param url: to get img url
    :return: img
    """
    try:
        with request.urlopen(url) as img:
            img = img.read()
    except RuntimeError:
        img = b''
    return img


def find_text(pattern, text: str) -> str:
    """
    find text by pattern
    :param pattern: to get text pattern
    :param text: text
    :return: found text
    """
    if not isinstance(text, str):
        text = str(text)
    try:
        find_text_value = str(re.findall(rf'{pattern}', text)[0])
    except IndexError:
        find_text_value = ''
    return find_text_value


def get_music_id(title: str, artist: str, log: bool) -> int:
    """
    get music_id in melone
    :param title: title in mp3-file
    :param artist: artist in mp3-file
    :param log: to console-print
    :return: music_id
    """
    def _get_music_id(url: str, title: str, log: bool) -> int:
        soup = get_soup(url, 'get_music_id', log=log).select(".fc_gray")
        if len(soup) == 0:
            raise ValueError
        music_id_list = [int(find_text(r'melon.play.playSong\(\'.+?\',(.+?)\);', k)) for k in soup]
        title_list = [remove_text(str(j['title'])) for j in soup]
        soup.clear()
        music_id_list_ = [music_id_list[title_list.index(i)] for i in title_list if i is title]
        # album_list = [soup[i[0]].get_text() for i in enumerate(soup) if i[0] % 3 == 2]
        if len(music_id_list_) == 0:
            music_id_list_ = [music_id_list[title_list.index(i)]
                              for i in title_list if i in title or title in i]
        if len(music_id_list_) == 0:
            music_id = int(music_id_list[0])
        else:
            music_id = int(music_id_list_[0])
        return music_id

    def get_music_id_by_title(title: str, log: bool) -> int:
        url = MelonSong_tagUrl + quote(title)
        pprint(f"{title} : {url}", log=log)
        music_id = _get_music_id(url, title, log)
        return music_id

    def get_music_id_by_title_artist(title: str, artist: str, log: bool) -> int:
        if artist is None or artist == '':
            music_id = get_music_id_by_title(title, log)
        else:
            url = MelonSong_tagUrl + quote(title) + '+' + quote(artist)
            pprint(f"{title} + {artist} : {url}", log=log)
            music_id = _get_music_id(url, title, log)
        return music_id

    try:
        return get_music_id_by_title_artist(title, artist, log=log)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(re.sub(r'\(*\)*', '', title), artist, log=log)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(re.sub(r'\\([^)]*\\)+', '', title), artist, log=log)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(''.join(find_text('[가-힣]+', title)), artist, log=log)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(tran_text(title), artist, log=log)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(title, tran_text(artist), log=log)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(tran_text(title), tran_text(artist), log=log)
    except ValueError:
        pass
    try:
        return get_music_id_by_title(title, log=log)
    except ValueError as error:
        not_working_list(target)
        raise ValueError(f"{error}: Didn't search '{title}, {artist}'") from error


def get_metadata(target_mp3, log):
    """
    get metadata by title-mp3-file, artist-mp3-file in melon
    :param target_mp3:
    :param log:
    :return: music_id: int, album_artist: str, title: str, album_name: str,
    year, genre: str[YYYY-MM-DD], lyric: str, img: bytes,
    track_num: tuple[music, total-music], album_id: int
    """
    audio_tag = eyed3.load(target_mp3).tag
    artist_in_mp3 = str(audio_tag.artist)
    if artist_in_mp3 is None:
        artist_in_mp3 = ''
    for i in expect_artist:
        if i in artist_in_mp3:
            artist_in_mp3 = artist_in_mp3.replace(i, '')
    artist_in_mp3 = artist_name_list.get(artist_in_mp3, artist_in_mp3)
    title_in_mp3 = str(audio_tag.title)
    if title_in_mp3 == 'None' or title_in_mp3 is None:
        title_in_mp3 = str(audio_tag.album)
    music_id = get_music_id(title_in_mp3, artist_in_mp3, log=log)
    soup = get_soup(MelonSongUrl + str(music_id), 'get_tag', log=log)
    album_artist = soup.select('.artist_name')[0].get_text()
    title = soup.select('.song_name')[0].get_text().replace('곡명', '').strip()
    album_name = soup.select('.list')[0]
    album_id = find_text(r'goAlbumDetail\(\'(.+?)\'\);', album_name)
    music_info = str(album_name.get_text()).replace('\n', '')
    album_names = find_text('앨범(.+?)발매일', music_info)
    year = find_text('발매일(.+?)장르', music_info).replace('.', '-')
    if 'FLAC' in music_info:
        genre = find_text('장르(.+?)FLAC', music_info)
    else:
        genre = find_text('장르(.+?)$', music_info)
    for i in soup.find_all('br'):  # 추후 개선
        i.replace_with('\n')
    try:
        lyric = soup.select(".lyric")[0].get_text().strip()
    except RuntimeError:
        pprint('No lyric')
        lyric = ''
    finally:
        soup.clear()
    if '19금' in title:
        pprint(f'Do not get metadata, because "{title}" is music of only-adult')
        title = str(title).lstrip('19금').strip()
    try:
        url = MelonAlbumUrl + str(album_id)
        soup = get_soup(url, 'get_album_img', log=log)
    except ValueError:
        url = MelonAlbumUrl + str(album_id[:album_id_short])
        soup = get_soup(url, 'get_album_img', log=log)
    album_img = soup.select('meta[property="og:image"]')[0]
    pprint(f'album : {url}', log=log)
    urls = find_text('(?:(?:https?|ftp)://)?[\\w/\\-?=%.]+\\.[\\w/\\-?=%.]+', album_img)
    try:
        img = get_img_by_url(urls.replace('500.jpg', '1000.jpg'))
    except RuntimeError:
        img = get_img_by_url(urls)
    pprint(f'album img url : {urls}', log=log)
    title_in_album = []
    for i in soup.select('.wrap_song_info'):
        temp_title_in_album = find_text('>(.+?)</a>', i)
        if '&amp;' in temp_title_in_album:
            temp_title_in_album = temp_title_in_album.replace('&amp;', '&')
        if '(Inst.)' not in temp_title_in_album:
            title_in_album.append(temp_title_in_album)
    soup.clear()
    pprint(title_in_album, log=log)
    track_num = ((int(title_in_album.index(title)) + 1), len(title_in_album))
    return music_id, album_artist, title, album_names, year, genre, lyric, img, track_num, album_id
