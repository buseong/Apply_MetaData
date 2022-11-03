import os
import re
from random import randint
from urllib import request
from urllib.parse import quote

import eyed3
from bs4 import BeautifulSoup
from eyed3.id3.frames import ImageFrame

from .Data import *


def get_soup(url: str, usage: str):
    opener = request.build_opener()
    header = headers[randint(0, len(headers) - 1)]
    opener.addheaders = header
    request.install_opener(opener)
    html = request.urlopen(url)
    Soup = BeautifulSoup(html.read(), "html.parser")
    print(f"{usage} : {url}")
    html.close()
    return Soup


def _get_music_id(url: str, title: str) -> int:
    soup = get_soup(url, 'get_melon_info').select(".fc_gray")
    music_id_list = [int(re.findall(r'melon.play.playSong\(\'.+?\',(.+?)\);', str(k))[0]) for k in soup]
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


def get_music_id_by_title_artist(title: str, artist: str) -> int:
    url = "https://www.melon.com/search/song/index.htm?q=" + quote(title) + '+' + quote(artist)
    print(f"{title} + {artist} : {url}")
    music_id = _get_music_id(url, title)
    return music_id


def get_music_id_by_title(title: str) -> int:
    url = "https://www.melon.com/search/song/index.htm?q=" + quote(title)
    print(f"{title} : {url}")
    music_id = _get_music_id(url, title)
    return music_id


def get_music_id(music_info: tuple) -> int:
    title = music_info[0]
    artist = music_info[1]
    try:
        return get_music_id_by_title_artist(re.sub('\(*\)*', '', title), artist)
    except(Exception,):
        try:
            return get_music_id_by_title_artist(re.sub('\\([^)]*\\)+', '', title), artist)
        except(Exception,):
            try:
                return get_music_id_by_title_artist(' '.join(re.findall(r'[가-힣]+', title)), artist)
            except(Exception,):
                try:
                    return get_music_id_by_title(title)
                except(Exception,):
                    raise ValueError(f"Didn't search {title}, {artist}")


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


def get_text_re(pattern, text) -> str:
    after_text = str(re.findall(pattern, text)[0])
    return after_text


def get_tag(music_id: int, target: str) -> str or int:
    url = "https://www.melon.com/song/detail.htm?songId=" + str(music_id)
    soup = get_soup(url, 'get_tag')
    album_artist = soup.select('.artist_name')[0].get_text()
    title = soup.select('.song_name')[0].get_text().replace('곡명', '').strip()
    album_name = soup.select('.list')[0]
    music_info = str(album_name.get_text()).replace("\n", '')
    album_id = re.findall('goAlbumDetail\(\'(.+?)\'\);', str(album_name))[0]
    album_names = re.findall("앨범(.+?)발매일", music_info)[0]
    year = re.findall("발매일(.+?)장르", music_info)[0].replace('.', '-')
    if 'FLAC' in music_info:
        genre = re.findall("장르(.+?)FLAC", music_info)[0]
    else:
        genre = re.findall("장르(.+?)$", music_info)[0]
    for i in soup.find_all("br"):
        i.replace_with("\n")
    try:
        lyric = soup.select(".lyric")[0].get_text().strip()
    except(Exception,) as e:
        print('No lyric')
        print(e)
        lyric = ''
    if '19금' in title:
        raise ValueError("Don't get metadata")
    print(album_names, album_artist, title, album_id, year, genre)
    return album_names, album_artist, title, album_id, year, genre, lyric


def get_image_N_track(album_id: str or int, title: str) -> bytes and tuple:
    try:
        url = "https://www.melon.com/album/detail.htm?albumId=" + str(album_id)
        soup = get_soup(url, 'get_album_img')
    except(Exception,):
        url = "https://www.melon.com/album/detail.htm?albumId=" + str(album_id[:album_id_short])
        soup = get_soup(url, 'get_album_img')
    album_img = soup.select('meta[property="og:image"]')[0]
    print(f"album : {url}")
    urls = re.findall("(?:(?:https?|ftp)://)?[\\w/\\-?=%.]+\\.[\\w/\\-?=%.]+", str(album_img))[0]
    try:
        urls = urls.replace('500.jpg', '1000.jpg')
        img = request.urlopen(urls).read()
    except(Exception,):
        img = request.urlopen(urls).read()
    print(f'album img url : {urls}')
    title_in_album = []
    for i in soup.select('.wrap_song_info'):
        ck_tmp = re.findall('>(.+?)</a>', str(i))[0]
        if '&amp;' in ck_tmp:
            ck_tmp = ck_tmp.replace('&amp;', '&')
        if '(Inst.)' not in ck_tmp:
            title_in_album.append(ck_tmp)
    print(title_in_album)
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
            print(f'{k} is not in {key_list}')
    audio_file.tag.save(encoding='utf-8')
    return


def start(target: str):
    print(target)
    album_name, album_artist, title, album_id, years, genre, lyric\
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
    return


def get_mp3_address(target: str) -> list:
    folder = target.replace("\\", "/") + '/'
    now_file_edit = [folder + i for i in os.listdir(folder) if os.path.splitext(i)[1] == '.mp3']
    return now_file_edit
