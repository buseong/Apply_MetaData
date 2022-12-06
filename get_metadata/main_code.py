"""
Made By Buseong
"""
import re
from urllib.parse import quote

import eyed3
from eyed3.id3.frames import ImageFrame
from .utill.error_class import *
from .Data import *
from .utill.utill import (
    get_soup,
    get_img_by_url,
    check_type,
    pprint,
    remove_text,
    tran_text,
    find_text
    )

not_work_list = []


def not_working_list(target: str = None):
    """
    if target-instance is None, return "not_work_list": list
    if target-instance is not None, append target-instance to not_work_list
    :param target: file not running explorer address
    :return: not_work_list
    """
    if target is None:
        return not_work_list
    not_work_list.append(str(target))
    return None


def get_music_id(music_info: tuple[str, str], target: str) -> int:
    """
    find music-id by title or artist
    :param music_info: (title, artist) if artist is not found, artist = None
    :param target: to append 'not_working_list'-instance
    :return: music-id in melon
    """
    title = music_info[0]
    artist = music_info[1]

    check_type(target, str)
    check_type(title, str)
    check_type(artist, str)

    def _get_music_id(url: str, title: str) -> int or None:
        """
        get music_id
        :param url:
        :param title:
        :return: music_id but if soup is empty: return None
        """
        def remove_blank(text: str) -> str:
            return str(text).replace(' ', '')
        title = remove_blank(title)
        soup = get_soup(url, 'get_melon_info').select('.fc_gray')
        if len(soup) == 0:
            raise GetSoupError(f'Not found melone-music of music-tag in {target}')
        music_id_list = [int(find_text(r'melon.play.playSong\(\'.+?\',(.+?)\);', k)) for k in soup]
        title_list = [remove_text(remove_blank(j['title'])) for j in soup]
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

    def get_music_id_by_title(title: str) -> int or None:
        url = MelonSong_tagUrl + quote(title)
        pprint(f"{title} : {url}")
        return _get_music_id(url, title)

    def get_music_id_by_title_artist(title: str, artist: str) -> int or None:
        if artist is None or artist == 'None' or artist == '':
            return get_music_id_by_title(title)
        url = MelonSong_tagUrl + quote(title) + '+' + quote(artist)
        pprint(f'{title} + {artist} : {url}')
        return _get_music_id(url, title)

    search_error = SearchError

    try:
        return get_music_id_by_title_artist(title, artist)
    except search_error:
        pass
    try:
        return get_music_id_by_title_artist(re.sub(r'\(*\)*', '', title), artist)
    except search_error:
        pass
    try:
        return get_music_id_by_title_artist(re.sub(r'\(.+?\)$', '', title), artist)
    except search_error:
        pass
    try:
        return get_music_id_by_title_artist(''.join(find_text('[가-힣]+', title)), artist)
    except search_error:
        pass
    try:
        return get_music_id_by_title_artist(tran_text(title), artist)
    except search_error:
        pass
    try:
        return get_music_id_by_title_artist(title, tran_text(artist))
    except search_error:
        pass
    try:
        return get_music_id_by_title_artist(tran_text(title), tran_text(artist))
    except search_error:
        pass
    try:
        return get_music_id_by_title(title)
    except search_error as error:
        not_working_list(target)
        raise search_error(f'{error}: Did not search "{title}, {artist}"') from error


def get_title_artist_mp3(target_mp3: str) -> tuple[str, str]:
    """
    get title and artist in mp3
    :param target_mp3: to get title and artist
    :return: info(title, artist)
    """
    check_type(target_mp3, str)

    audio_tag = eyed3.load(target_mp3).tag
    artist = str(audio_tag.artist)
    if artist is None or artist == 'None':
        artist = ''
    for i in expect_artist:
        if i in artist:
            artist = artist.replace(i, '')
    # if artist in artist_name_list:
    #     artist = artist_name_list[artist]
    artist = str(artist_name_list.get(artist.strip(), artist))
    title = str(audio_tag.title)
    if title is None or title == 'None':
        title = str(audio_tag.album)
    return title, artist


def get_tag(music_id: str or int) -> str or int:
    """
    get tag by music_id
    :param music_id: to get tag music_id
    :return: album_names:str, album_artist:str, title:str,
            album_id:int, year:str, genre:str, lyric:str
    """
    assert isinstance(music_id, (str, int)), f'"{music_id}" is not str or int'
    adult_only = '19금'
    soup = get_soup(MelonSongUrl + str(music_id), 'get_tag')
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
    soup = soup.select(".lyric")
    try:
        if len(soup) == 0:
            raise IndexError('No lyric')
        soup = soup[0]
        for i in soup.find_all('br'):
            i.replace_with('\n')
        lyric = str(soup.get_text()).strip()
    except IndexError:
        pprint('No lyric')
        lyric = ''
    finally:
        soup.clear()
    if adult_only in title:
        title = str(title).lstrip(adult_only).strip()
        pprint(f'Do not get metadata, because "{title}" is music of only-adult')
    return album_names, album_artist, title, album_id, year, genre, lyric


def get_album_img(album_id: str or int) -> bytes:
    """
    get album img by album_id-instance
    :param album_id: to get album_img
    :return: album_img
    """
    assert isinstance(album_id, (str, int)), f'"{album_id}" is not str or int'
    try:
        url = MelonAlbumUrl + str(album_id)
        soup = get_soup(url, 'get_album_img')
    except GetInfoError:
        url = MelonAlbumUrl + str(album_id[:album_id_short])
        soup = get_soup(url, 'get_album_img')
    album_img = soup.select('meta[property="og:image"]')[0]
    pprint(f"album : {url}")
    # url = find_text('(?:(?:https?|ftp)://)?[\\w/\\-?=%.]+\\.[\\w/\\-?=%.]+', album_img)
    url = find_text('content="(.+?)"', album_img)
    try:
        img = get_img_by_url(url.replace('500.jpg', '1000.jpg'))
    except GetInfoError:
        img = get_img_by_url(url)
    pprint(f'album img url : {url}')
    return img


def get_track_num(album_id: str or int, title: str) -> tuple:
    """
    get track_num
    :param album_id: album-id
    :param title: title of music in album
    :return: (music, total-music)
    """
    assert isinstance(album_id, (str, int)), f'"{album_id}" is not str or int'
    check_type(title, str)
    try:
        url = MelonAlbumUrl + str(album_id)
        soup = get_soup(url, 'get_album_img')
    except GetInfoError:
        url = MelonAlbumUrl + str(album_id[:album_id_short])
        soup = get_soup(url, 'get_album_img')
    title_in_album = []
    for i in soup.select('.wrap_song_info'):
        temp_title_in_album = find_text('>(.+?)</a>', i)
        if '&amp;' in temp_title_in_album:
            temp_title_in_album = temp_title_in_album.replace('&amp;', '&')
        if '(Inst.)' not in temp_title_in_album:
            title_in_album.append(temp_title_in_album)
    track_num = ((int(title_in_album.index(title)) + 1), len(title_in_album))
    return track_num


def save_tag(target: str, **kwargs: dict):
    """
    save tag
    :param target: to save mp3-file
    :param kwargs: to save tag in mp3-file
    """
    check_type(target, str)
    eyed3.log.setLevel("ERROR")
    audio_file = eyed3.load(target)
    if not audio_file.tag:
        audio_file.initTag()
    for key, value in kwargs.items():
        if key in tag_list:
            if key == 'lyrics':
                audio_file.tag.lyrics.set(value)
            elif key == 'track_num':
                audio_file.tag.track_num = value
            elif key == 'image':
                audio_file.tag.images.set(ImageFrame.FRONT_COVER, value, 'image/jpeg')
            else:
                setattr(audio_file.tag, key, value)
        else:
            pprint(f'{key} is not in {tag_list}')
    audio_file.tag.save(encoding='utf-8')


def tag_output_reformat(album_name: str = None,
                        album_artist: str = None,
                        title: str = None,
                        genre: str = None,
                        lyrics: str = None,
                        recording_data: str = None,
                        track_num: tuple = None,
                        image: bytes = None,
                        artist: str = None
                        ) -> dict:
    """
    reformat for tag,
    artist and album_artist is None: artist = album_artist = ''
    album_artist is None: album_artist = artist
    artist is None: artist = album_artist
    :param title: str
    :param genre:str
    :param lyrics: str
    :param artist: str
    :param album_name: str
    :param album_artist: str
    :param recording_data: str[YYYY-MM-DD]
    :param track_num: tuple[num, total_num]
    :param image: bytes
    :return: reformat-tag
    """
    if artist is None:
        if album_artist is None:
            album_artist = ''
        artist = album_artist
    else:
        if album_artist is None:
            album_artist = artist
    metadata_info: dict = {
        'album': album_name,
        'album_artist': album_artist,
        'title': title,
        'image': image,
        'genre': genre,
        'recording_date': recording_data,
        'lyrics': lyrics,
        'track_num': track_num,
        'artist': artist,
    }
    return metadata_info


def start(target: str, return_bool: bool = False):
    """
    start get-metadata
    :param target: to save metadata target-instance
    :param return_bool: to return metadata info
    :return: return metadata
    """
    check_type(target, str)
    pprint(target)
    album_name, album_artist, title, album_id, years, genre, lyric \
        = get_tag(get_music_id(get_title_artist_mp3(target), target))
    img = get_album_img(album_id)
    track_num = get_track_num(album_id, title)
    metadata_info = tag_output_reformat(
        album_name=album_name, album_artist=album_artist,
        title=title, genre=genre,
        lyrics=lyric, recording_data=years,
        track_num=track_num, image=img
                                        )
    pprint(not_working_list())
    if return_bool:
        return metadata_info
    save_tag(target=target, **metadata_info)
    return None
