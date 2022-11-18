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

not_Work = []


def get_soup(url: str, usage: str):
    opener = request.build_opener()
    header = headers[randint(0, len(headers) - 1)]
    opener.addheaders = header
    request.install_opener(opener)
    html = request.urlopen(url)
    Soup = BeautifulSoup(html.read(), "html.parser")
    pprint(f"{usage} : {url}")
    html.close()
    return Soup


def pprint(text, types=...):
    necessary_types = ['log']
    if types is ...:
        print(text)
        # ...
    elif types in necessary_types:
        print(text)
    else:
        print(types, text)
    return


def _get_music_id(url: str, title: str) -> int:
    soup = get_soup(url, 'get_melon_info').select(".fc_gray")
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


def insert_Url(*args) -> str:
    args_convert = [quote(i) for i in args]
    url = ' + '.join(args_convert)
    return url


def get_music_id_by_title_artist(title: str, artist: str) -> int:
    url = MelonSong_tagUrl + quote(title) + '+' + quote(artist)
    pprint(f"{title} + {artist} : {url}")
    music_id = _get_music_id(url, title)
    return music_id


def get_music_id_by_title(title: str) -> int:
    url = MelonSong_tagUrl + quote(title)
    pprint(f"{title} : {url}")
    music_id = _get_music_id(url, title)
    return music_id


def not_working_list(target: str = ...):
    if target is ...:
        return not_Work
    else:
        not_Work.append(str(target))
        return


# def _search_algorithm(title: str = ..., artist: str = ...):
#     try:
#         if title is not ... and artist is not ...:
#             return get_music_id_by_title_artist(title, artist)
#         elif title is not ...:
#             return get_music_id_by_title(title)
#         else:
#             pprint(f"Didn't search {title}, {artist}")
#     except ValueError:
#         pass


def get_music_id(music_info: tuple) -> int:
    title = music_info[0]
    artist = music_info[1]
    try:
        return get_music_id_by_title_artist(title, artist)
    except:
        try:
            return get_music_id_by_title_artist(re.sub('\(*\)*', '', title), artist)
        except:
            try:
                return get_music_id_by_title_artist(re.sub('\\([^)]*\\)+', '', title), artist)
            except:
                try:
                    return get_music_id_by_title_artist(''.join(find_textByRe('[가-힣]+', title)), artist)
                except:
                    try:
                        return get_music_id_by_title_artist(tran_Text(title)[0], artist)
                    except:
                        try:
                            return get_music_id_by_title_artist(title, tran_Text(artist)[0])
                        except:
                            try:
                                return get_music_id_by_title_artist(tran_Text(title)[0], tran_Text(artist)[0])
                            except:
                                try:
                                    return get_music_id_by_title(title)
                                except:
                                    raise ValueError(f"Didn't search {title}, {artist}")


def tran_Text(*args: tuple) -> list:
    result = [str(Translator().translate(i, src='en', dest='ko').text).strip() for i in args]
    pprint(f'{args} -> {result}')
    return result


def get_title_artist_mp3(target_mp3: str) -> tuple:
    audio_tag = eyed3.load(target_mp3).tag
    artist = str(audio_tag.artist)
    if artist is None or '':
        artist = ''
    if ' - Topic' in artist:
        artist = artist.rstrip(" - Topic")
    if artist in artist_name_list:
        artist = artist_name_list[artist]
    title = str(audio_tag.title)
    if title == 'None' or None:
        title = str(audio_tag.album)
    info = (title, artist)
    return info


def find_textByRe(pattern, text) -> str:
    if not isinstance(text, str):
        text = str(text)
    try:
        find_text = str(re.findall(rf'{pattern}', text)[0])
    except:
        find_text = ''
    return find_text


def get_tag(music_id: int or str, target: str) -> int or str:
    url = MelonSongUrl + str(music_id)
    soup = get_soup(url, 'get_tag')
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
        pprint('No lyric', 'get_tag')
        lyric = ''
    if '19금' in title:
        pprint(f"Don't get metadata, because '{title}' is music of only-adult", 'get_tag')
        title = str(title).lstrip('19금').strip()
    return album_names, album_artist, title, album_id, year, genre, lyric


def get_imgByUrl(url: str) -> bytes:
    try:
        img = request.urlopen(url).read()
    except:
        img = b''
    return img


def get_image_N_track(album_id: str or int, title: str) -> bytes and tuple:
    try:
        url = MelonAlbumUrl + str(album_id)
        soup = get_soup(url, 'get_album_img')
    except:
        url = MelonAlbumUrl + str(album_id[:album_id_short])
        soup = get_soup(url, 'get_album_img')
    album_img = soup.select('meta[property="og:image"]')[0]
    pprint(f"album : {url}")
    urls = find_textByRe('(?:(?:https?|ftp)://)?[\\w/\\-?=%.]+\\.[\\w/\\-?=%.]+', album_img)
    try:
        img = get_imgByUrl(urls.replace('500.jpg', '1000.jpg'))
    except:
        img = get_imgByUrl(urls)
    pprint(f'album img url : {urls}')
    title_in_album = []
    for i in soup.select('.wrap_song_info'):
        _titleInAlbum = find_textByRe('>(.+?)</a>', i)
        if '&amp;' in _titleInAlbum:
            _titleInAlbum = _titleInAlbum.replace('&amp;', '&')
        if '(Inst.)' not in _titleInAlbum:
            title_in_album.append(_titleInAlbum)
    pprint(title_in_album)
    track_num = ((int(title_in_album.index(title)) + 1), len(title_in_album))
    return img, track_num


def save_tag(target, **kwargs):
    eyed3.log.setLevel("ERROR")
    audio_file = eyed3.load(target)
    if not audio_file.tag:
        audio_file.initTag()
    for k, v in kwargs.items():
        if k in key_list:
            if k == 'lyrics':
                audio_file.tag.lyrics.set(v)
            elif k == 'track_num':
                audio_file.tag.track_num = v
            elif k == 'image':
                audio_file.tag.images.set(ImageFrame.FRONT_COVER, v, 'image/jpeg')
            else:
                exec(f'audio_file.tag.{k} = "{v}"')
        else:
            pprint(f'{k} is not in {key_list}')
    audio_file.tag.save(encoding='utf-8')
    return


def start(target: str):
    pprint(target)
    album_name, album_artist, title, album_id, years, genre, lyric \
        = get_tag(get_music_id(get_title_artist_mp3(target)), target)
    img, track_num = get_image_N_track(album_id, title)
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
    return


def get_mp3_address(target: str) -> list:
    if not isinstance(target, str):
        raise ValueError(f'{target} is not string, {type(target)}')
    folder = target.replace("\\", "/") + '/'
    now_file_edit = [folder + i for i in listdir(folder) if path.splitext(i)[1] == '.mp3']
    return now_file_edit
