"""
Made By Buseong
"""
from os import path, listdir
import re
from random import randint
from urllib import request
from urllib.parse import quote

import eyed3
from bs4 import BeautifulSoup
from eyed3.id3.frames import ImageFrame
from googletrans import Translator

from .Data import *

not_work_list = []


def get_soup(url: str, usage: str):
    """
    get soup
    :param url: to get soup
    :param usage: to record where this function was executed
    :return: soup
    """
    pprint(f"{usage} : {url}")
    opener = request.build_opener()
    header = headers[randint(0, len(headers) - 1)]
    opener.addheaders = header
    request.install_opener(opener)
    with request.urlopen(url) as html:
        soup = BeautifulSoup(html.read(), "html.parser")
    return soup


def pprint(text, types: bool = True):
    """
    print text-instance but types-instance is False: Not print
    :param text: to print text
    :param types:
    """
    if types:
        print(text)
    else:
        pass


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


def get_music_id(music_info: tuple) -> int:
    """
    find music-id by title or artist
    :param music_info: (title, artist) if artist is not found, artist = None
    :return: music-id in melon
    """
    title = music_info[0]
    artist = music_info[1]

    def _get_music_id(url: str, title: str) -> int:
        soup = get_soup(url, 'get_melon_info').select(".fc_gray")
        if len(soup) == 0:
            raise ValueError
        music_id_list = [int(find_text(r'melon.play.playSong\(\'.+?\',(.+?)\);', k)) for k in soup]
        title_list = [remove_text(str(j['title'])) for j in soup]
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

    def get_music_id_by_title(title: str) -> int:
        url = MelonSong_tagUrl + quote(title)
        pprint(f"{title} : {url}")
        music_id = _get_music_id(url, title)
        return music_id

    def get_music_id_by_title_artist(title: str, artist: str) -> int:
        if artist is None or artist == '':
            music_id = get_music_id_by_title(title)
        else:
            url = MelonSong_tagUrl + quote(title) + '+' + quote(artist)
            pprint(f"{title} + {artist} : {url}")
            music_id = _get_music_id(url, title)
        return music_id

    try:
        return get_music_id_by_title_artist(title, artist)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(re.sub(r'\(*\)*', '', title), artist)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(re.sub(r'\\([^)]*\\)+', '', title), artist)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(''.join(find_text('[가-힣]+', title)), artist)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(tran_text(title), artist)
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(title, tran_text(artist))
    except ValueError:
        pass
    try:
        return get_music_id_by_title_artist(tran_text(title), tran_text(artist))
    except ValueError:
        pass
    try:
        return get_music_id_by_title(title)
    except ValueError as error:
        raise ValueError(f"{error}: Didn't search '{title}, {artist}'") from error


def spilt_text(text: str, spilt_t: str) -> list:
    """
    spilt text
    :param text: text to divide
    :param spilt_t: to divide the text into
    :return: text
    """
    return text.split(spilt_t)


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


def get_title_artist_mp3(target_mp3: str) -> tuple:
    """
    get title and artist in mp3
    :param target_mp3: to get title and artist
    :return: info(title, artist)
    """
    audio_tag = eyed3.load(target_mp3).tag
    artist = str(audio_tag.artist)
    if artist is None:
        artist = ''
    for i in expect_artist:
        if i in artist:
            artist = artist.replace(i, '')
    if artist in artist_name_list:
        artist = artist_name_list[artist]
    title = str(audio_tag.title)
    if title is None or 'None':
        title = str(audio_tag.album)
    info = (title, artist)
    return info


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
        find_text = str(re.findall(rf'{pattern}', text)[0])
    except IndexError:
        find_text = ''
    return find_text


def get_tag(music_id: int or str) -> int or str:
    """
    get tag by music_id
    :param music_id: to get tag music_id
    :return: album_names:str, album_artist:str, title:str, album_id:int, year:str, genre:str, lyric:str
    """
    url = MelonSongUrl + str(music_id)
    soup = get_soup(url, 'get_tag')
    album_artist = soup.select('.artist_name')[0].get_text()
    title = soup.select('.song_name')[0].get_text().replace('곡명', '').strip()
    album_name = soup.select('.list')[0]
    music_info = str(album_name.get_text()).replace("\n", '')
    album_id = find_text(r'goAlbumDetail\(\'(.+?)\'\);', album_name)
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
    if '19금' in title:
        pprint(f"Don't get metadata, because '{title}' is music of only-adult")
        title = str(title).lstrip('19금').strip()
    return album_names, album_artist, title, album_id, year, genre, lyric


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


def get_album_img(album_id: str or int) -> bytes:
    """
    get album img by album_id-instance
    :param album_id: to get album_img
    :return: album_img
    """
    try:
        url = MelonAlbumUrl + str(album_id)
        soup = get_soup(url, 'get_album_img')
    except ValueError:
        url = MelonAlbumUrl + str(album_id[:album_id_short])
        soup = get_soup(url, 'get_album_img')
    album_img = soup.select('meta[property="og:image"]')[0]
    pprint(f"album : {url}")
    urls = find_text('(?:(?:https?|ftp)://)?[\\w/\\-?=%.]+\\.[\\w/\\-?=%.]+', album_img)
    try:
        img = get_img_by_url(urls.replace('500.jpg', '1000.jpg'))
    except RuntimeError:
        img = get_img_by_url(urls)
    pprint(f'album img url : {urls}')
    return img


def get_track_num(album_id: str or int, title: str) -> tuple:
    """
    get track_num
    :param album_id: album-id
    :param title: title of music in album
    :return: (music, total-music)
    """
    try:
        url = MelonAlbumUrl + str(album_id)
        soup = get_soup(url, 'get_album_img')
    except ValueError:
        url = MelonAlbumUrl + str(album_id[:album_id_short])
        soup = get_soup(url, 'get_album_img')
    title_in_album = []
    for i in soup.select('.wrap_song_info'):
        temp_title_in_album = find_text('>(.+?)</a>', i)
        if '&amp;' in temp_title_in_album:
            temp_title_in_album = temp_title_in_album.replace('&amp;', '&')
        if '(Inst.)' not in temp_title_in_album:
            title_in_album.append(temp_title_in_album)
    pprint(title_in_album)
    track_num = ((int(title_in_album.index(title)) + 1), len(title_in_album))
    return track_num


def save_tag(target, **kwargs):
    """
    save tag
    :param target: to save mp3-file
    :param kwargs: to save tag in mp3-file
    """
    eyed3.log.setLevel("ERROR")
    audio_file = eyed3.load(target)
    if not audio_file.tag:
        audio_file.initTag()
    for key, value in kwargs.items():
        if key in key_list:
            if key == 'lyrics':
                audio_file.tag.lyrics.set(value)
            elif key == 'track_num':
                audio_file.tag.track_num = value
            elif key == 'image':
                audio_file.tag.images.set(ImageFrame.FRONT_COVER, value, 'image/jpeg')
            else:
                exec(f'audio_file.tag.{key} = "{value}"')
        else:
            pprint(f'{key} is not in {key_list}')
    audio_file.tag.save(encoding='utf-8')


def start(target: str):
    """
    start get-metadata
    :param target: to save metadata target-instance
    """
    pprint(target)
    album_name, album_artist, title, album_id, years, genre, lyric \
        = get_tag(get_music_id(get_title_artist_mp3(target)))
    img = get_album_img(album_id)
    track_num = get_track_num(album_id, title)
    save_tag(
        album=album_name,
        album_artist=album_artist,
        title=title,
        image=img,
        target=target,
        genre=genre,
        recording_date=years,
        lyrics=lyric,
        track_num=track_num,
        artist=album_artist
    )
    pprint(not_working_list())


def get_mp3_address(target: str) -> list:
    """
    get address-mp3-file
    :param target: to get explorer-address
    :return: list-mp3-file
    """
    if not isinstance(target, str):
        raise ValueError(f'{target} is not string, {type(target)}')
    folder = target.replace("\\", "/") + '/'
    now_file_edit = [folder + i for i in listdir(folder) if path.splitext(i)[1] == '.mp3']
    return now_file_edit
