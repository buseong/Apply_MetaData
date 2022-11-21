import re
from random import randint
from urllib import request
from urllib.parse import quote

import eyed3
from bs4 import BeautifulSoup
from googletrans import Translator

from .Data import *

not_Work = []


def get_soup(url: str, usage: str, log: bool):
    opener = request.build_opener()
    header = headers[randint(0, len(headers) - 1)]
    opener.addheaders = header
    request.install_opener(opener)
    html = request.urlopen(url)
    Soup = BeautifulSoup(html.read(), "html.parser")
    pprint(log, f"{usage} : {url}")
    html.close()
    return Soup


def pprint(log, *args):
    if log:
        if len(args) == 1:
            print(args[0])
        else:
            for i in args:
                print(i, end=' | ')
    else:
        pass


def not_working_list(target: str = ...):
    if target is ...:
        return not_Work
    else:
        not_Work.append(str(target))
        return


def tran_Text(*args: tuple) -> list:
    result = [str(Translator().translate(i, src='en', dest='ko').text).strip() for i in args]
    pprint(f'{args} -> {result}')
    return result


def get_imgByUrl(url: str) -> bytes:
    try:
        img = request.urlopen(url).read()
    except:
        img = b''
    return img


def find_textByRe(pattern, text) -> str:
    if not isinstance(text, str):
        text = str(text)
    try:
        find_text = str(re.findall(rf'{pattern}', text)[0])
    except:
        find_text = ''
    return find_text


def _get_music_id(url: str, title: str, log: bool) -> int:
    soup = get_soup(url, 'get_melon_info', log).select(".fc_gray")
    music_id_list = [int(find_textByRe('melon.play.playSong\(\'.+?\',(.+?)\);', k)) for k in soup]
    title_list = [str(j['title']).rstrip(' - 페이지 이동') for j in soup]
    music_id_list_ = [music_id_list[title_list.index(i)] for i in title_list if i is title]
    # album_list = [soup[i[0]].get_text() for i in enumerate(soup) if i[0] % 3 == 2]
    if len(music_id_list_) == 0:
        music_id_list_ = [music_id_list[title_list.index(i)] for i in title_list if i in title or title in i]
    if len(music_id_list_) == 0:
        music_id = int(music_id_list[0])
    else:
        music_id = int(music_id_list_[0])
    return music_id


def get_music_id_by_title_artist(title: str, artist: str, log: bool) -> int:
    url = MelonSong_tagUrl + quote(title) + '+' + quote(artist)
    pprint(log, f"{title} + {artist} : {url}")
    music_id = _get_music_id(url, title, log=log)
    return music_id


def get_music_id_by_title(title: str, log: bool) -> int:
    url = MelonSong_tagUrl + quote(title)
    pprint(log, f"{title} : {url}")
    music_id = _get_music_id(url, title, log=log)
    return music_id


def get_music_id(title, artist, log: bool) -> int:
    try:
        return get_music_id_by_title_artist(title, artist, log=log)
    except:
        try:
            return get_music_id_by_title_artist(re.sub('\(*\)*', '', title), artist, log=log)
        except:
            try:
                return get_music_id_by_title_artist(re.sub('\\([^)]*\\)+', '', title), artist, log=log)
            except:
                try:
                    return get_music_id_by_title_artist(''.join(find_textByRe('[가-힣]+', title)), artist, log=log)
                except:
                    try:
                        return get_music_id_by_title_artist(tran_Text(title)[0], artist, log=log)
                    except:
                        try:
                            return get_music_id_by_title_artist(title, tran_Text(artist)[0], log=log)
                        except:
                            try:
                                return get_music_id_by_title_artist(tran_Text(title)[0], tran_Text(artist)[0], log=log)
                            except:
                                try:
                                    return get_music_id_by_title(title, log=log)
                                except:
                                    raise ValueError(f"Didn't search {title}, {artist}")


def get_metadata(target_mp3, log):
    audio_tag = eyed3.load(target_mp3).tag
    artist_in_mp3 = str(audio_tag.artist)
    if artist_in_mp3 is None or '':
        artist_in_mp3 = ''
    if ' - Topic' in artist_in_mp3:
        artist_in_mp3 = artist_in_mp3.rstrip(" - Topic")
    if artist_in_mp3 in artist_name_list:
        artist_in_mp3 = artist_name_list[artist_in_mp3]
    title_in_mp3 = str(audio_tag.title)
    if title_in_mp3 == 'None' or None:
        title_in_mp3 = str(audio_tag.album)
    music_id = get_music_id(title_in_mp3, artist_in_mp3, log)
    soup = get_soup(MelonSongUrl + str(music_id), 'get_tag', log)
    album_artist = soup.select('.artist_name')[0].get_text()
    title = soup.select('.song_name')[0].get_text().replace('곡명', '').strip()
    album_name = soup.select('.list')[0]
    music_info = str(album_name.get_text()).replace("\n", '')
    album_id = find_textByRe('goAlbumDetail\(\'(.+?)\'\);', album_name)
    album_names = find_textByRe('앨범(.+?)발매일', music_info)
    year = find_textByRe('발매일(.+?)장르', music_info).replace('.', '-')
    if 'FLAC' in music_info:
        genre = find_textByRe('장르(.+?)FLAC', music_info)
    else:
        genre = find_textByRe('장르(.+?)$', music_info)
    for i in soup.find_all('br'):
        i.replace_with('\n')
    try:
        lyric = soup.select(".lyric")[0].get_text().strip()
    except:
        pprint(log, 'No lyric')
        lyric = ''
    if '19금' in title:
        pprint(log, f"Don't get metadata, because '{title}' is music of only-adult")
        title = str(title).lstrip('19금').strip()
    try:
        url = MelonAlbumUrl + str(album_id)
        soup = get_soup(url, 'get_album_img',log)
    except:
        url = MelonAlbumUrl + str(album_id[:album_id_short])
        soup = get_soup(url, 'get_album_img', log)
    album_img = soup.select('meta[property="og:image"]')[0]
    pprint(f"album : {url}")
    url = find_textByRe('(?:(?:https?|ftp)://)?[\\w/\\-?=%.]+\\.[\\w/\\-?=%.]+', album_img)
    try:
        img = get_imgByUrl(url.replace('500.jpg', '1000.jpg'))
    except:
        img = get_imgByUrl(url)
    pprint(log, f'album img url : {url}')
    title_in_album = []
    for i in soup.select('.wrap_song_info'):
        _titleInAlbum = find_textByRe('>(.+?)</a>', i)
        if '&amp;' in _titleInAlbum:
            _titleInAlbum = _titleInAlbum.replace('&amp;', '&')
        if '(Inst.)' not in _titleInAlbum:
            title_in_album.append(_titleInAlbum)
    pprint(log, title_in_album)
    track_num = ((int(title_in_album.index(title)) + 1), len(title_in_album))
    return music_id, album_artist, title, album_names, year, genre, lyric, img, track_num, album_id
