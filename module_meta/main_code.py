"""
Made by Buseong
2022-10-20
ver 0.12.10
"""
import os
import re
from random import randint
from urllib import request
from urllib.parse import quote

import eyed3
from bs4 import BeautifulSoup
from eyed3.id3.frames import ImageFrame

from Data import *

arr_work: list = []


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


def get_music_id(title: str, artist: str = '') -> int:
    print(title, artist)
    if artist != '':
        url = "https://www.melon.com/search/song/index.htm?q=" + quote(title) \
              + '+' + quote(artist)
        print(f"{title} + {artist} : {url}")
    else:
        url = "https://www.melon.com/search/song/index.htm?q=" + quote(title)
        print(f"{title} : {url}")
    soup = get_soup(url, 'get_melon_info')
    music_id_list = [int(re.findall('\'(.+?)\'', str(re.findall(r'searchLog\((.+?)\);', k['href'])[0]).split(',')[music_id_l])[0]) for k in soup.select(".fc_gray")]
    # album_list = [soup.select('.fc_mgray')[i].get_text() for i in range(len(soup.select(".fc_mgray"))) if i % 3 == 2]
    title_list = [str(j['title']).rstrip(' - 페이지 이동') for j in soup.select(".fc_gray")]
    _music_id = [music_id_list[title_list.index(i)] for i in title_list if i == title]
    if len(_music_id) == 0:
        _music_id = [music_id_list[title_list.index(i)] for i in title_list if i in title or title in i]
    if len(_music_id) == 0:
        music_id = int(music_id_list[0])
    else:
        music_id = int(_music_id[0])
    return music_id


def get_title_artist(music_info: tuple) -> int:
    title = music_info[0]
    artist = music_info[1]
    try:
        title = re.sub('\(*\)*', '', title)
        if 'Instrumental' in title:
            title = title.rstrip('Instrumental')
        print(title)
        return get_music_id(title=title, artist=artist)
    except(Exception,):
        try:
            return get_music_id(title=' '.join(re.findall(r'[가-힣]+', title)), artist=artist)
        except(Exception,):
            try:
                return get_music_id(title=title)
            except(Exception,):
                try:
                    return get_music_id(title=re.sub('\\([^)]*\\)', '', title), artist=artist)
                except(Exception,):
                    raise ValueError(f"Didn't search {title}, {artist}")


def get_title_artist_mp3(target_mp3: str) -> tuple:
    audio_tag = eyed3.load(target_mp3).tag
    artist = str(audio_tag.artist)
    if artist is None or '':
        artist = ''
    if ' - Topic' in artist:
        artist = artist.rstrip(" - Topic")
    if artist in tran_name:
        artist = tran_name[artist]
    title = str(audio_tag.title)
    if title == 'None' or None:
        title = str(audio_tag.album)
    info = (title, artist)
    return info


def get_tag(music_id: int, target: str) -> str or int:
    url = "https://www.melon.com/song/detail.htm?songId=" + str(music_id)
    soup = get_soup(url, 'get_tag')
    album_artist = soup.select('.artist_name')[0].get_text()
    title = soup.select('.song_name')[0].get_text().replace('곡명', '').strip()
    album_name = soup.select('.list')[0]
    album_name_ = str(album_name.get_text()).replace("\n", '')
    album_id = ''.join(re.findall("[0-9]", str(re.findall('href="(.+?)"', str(album_name).replace("\n", '')))))
    album_names = re.findall("앨범(.+?)발매일", album_name_)[0]
    year = re.findall("발매일(.+?)장르", album_name_)[0].replace('.', '-')
    if 'FLAC' in album_name_:
        genre = re.findall("장르(.+?)FLAC", album_name_)[0]
    else:
        genre = re.findall("장르(.+?)$", album_name_)[0]
    for i in soup.find_all("br"):
        i.replace_with("\n")
    try:
        lyric = soup.select(".lyric")[0].get_text().strip()
    except(Exception,) as e:
        print('No lyric')
        print(e)
        arr_work.append(target)
        lyric = ''
    if '19금' in title:
        raise ValueError("Don't get metadata")
    print(album_names, album_artist, title, album_id, year, genre)
    return album_names, album_artist, title, album_id, year, genre, lyric


def get_artist(artist_id: int or str) -> bytes:
    url = 'https://www.melon.com/artist/timeline.htm?artistId=' + str(artist_id)
    print(url)
    soup = get_soup(url, 'get artist img')
    artist_img_url = soup.select('meta[property="og:image"]')[0]['content']
    print(artist_img_url)
    img = request.urlopen(artist_img_url).read()
    return img


def get_image_track(album_id: str or int, title: str) -> bytes or tuple:
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
                audio_file.tag.images.remove(u'')
                audio_file.tag.images.set(ImageFrame.FRONT_COVER, v, 'image/jpeg')
            else:
                exec(f'audio_file.tag.{k} = "{v}"')
    audio_file.tag.save(encoding='utf-8')
    return


def start(target: str):
    print(target)
    album_name, album_artist, title, album_id, years, genre, lyric\
        = get_tag(get_title_artist(get_title_artist_mp3(target)), target)
    img, track_num = get_image_track(album_id, title)
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


def get_mp3(target: str) -> list:
    folder = target.replace("\\", "/") + '/'
    now_file_edit = [folder + i for i in os.listdir(folder) if os.path.splitext(i)[1] == '.mp3']
    return now_file_edit


def check_meta(target):
    audio_file = eyed3.load(target)
    return (
            audio_file.tag.album_artist,
            audio_file.tag.title,
            audio_file.tag.album,
            audio_file.tag.genre,
            audio_file.tag.artist,
            audio_file.tag.recording_date,
            audio_file.tag.track_num,
            audio_file.tag.lyrics
            )
