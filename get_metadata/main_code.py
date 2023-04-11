"""
Made By Buseong
"""
from re import sub
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
    # check_type((title, artist, target), str)

    work_list = []

    def check_work(work):
        pprint(work)
        if work in work_list:
            return True
        work_list.append(work)
        return False

    def _get_music_id(url: str, title: str, org_title: str, artist: str) -> int or None:
        """
        get music_id
        :param url: to search url
        :param title: to search-instance title
        :return: music_id but if soup is empty: ValueError
        """

        def remove_blank(text: str) -> str:
            return str(text).replace(' ', '')

        def special_characters_remove(text):
            arr = {
                "cant": "can't",
                "dont": "don't",
                "didnt": "didn't",
                "couldnt": "couldn't",
            }
            text = str(text).lower()
            for i, j in arr.items():
                if text.__contains__(j):
                    text = text.replace(j, i)
            return text

        def expect_string(text1: str, text2: str):
            text1 = remove_blank(text1.lower())
            text2 = remove_blank(text2.lower())

            arr = ["version", "ver.", "ver", 'inst.', 'inst', 'instrumental']
            for i in arr:
                if text1.__contains__(i):
                    for j in arr:
                        if text2.__contains__(j):
                            return True

        title = remove_blank(title).lower()
        artist = remove_blank(artist).lower()

        if artist.__eq__(""):
            artist = ""  # to None

        soup = get_soup(url, 'get_melon_info')

        if len(soup) == 0:
            raise GetSoupError('maybe internet-contact error or melon-sever down or ban')

        music_id_list = [int(find_text(r'melon.play.playSong\(\'.+?\',(.+?)\);', i)) for i in soup.select('.fc_gray')]

        if len(music_id_list).__eq__(0):
            raise GetSoupError(f'Not found melone-music of music-tag in {target}')

        title_list = [remove_text(remove_blank(i['title'])).lower() for i in soup.select('.fc_gray')]
        artist_list = [find_text('title=\"(.+?) - 페이지 이동\">', i).lower() for i in soup.select("#artistName")]
        del soup

        # music_id_list_acc = [music_id_list[title_list.index(i)] for i in title_list if i.lower().__contains__(special_characters_remove(title.lower()))]
        music_id_list_acc = []
        title_list_acc = []
        artist_list_acc = []
        # album_list = [soup[i[0]].get_text() for i in enumerate(soup) if i[0] % 3 == 2]
        for i, j in enumerate(title_list):
            if j.__contains__((_temp_title := special_characters_remove(title))) or _temp_title.__contains__(j):
                artist_list_acc.append(artist_list[i])
                music_id_list_acc.append(music_id_list[i])
                title_list_acc.append(title_list[i])

        # if len(music_id_list_acc) == 0:  # same len(artist_list_acc)
        #     music_id_list_acc = [music_id_list[title_list.index(i)]
        #                          for i in title_list if i.lower().__contains__(title.lower()) or title.lower().__contains__(i.lower())]
        for num, music_id in enumerate(music_id_list_acc):
            low_title = title_list_acc[num]
            low_artist = artist_list_acc[num]

            print(
                low_title.__contains__(title),
                low_title.__eq__(title),
                artist.__contains__(artist),
                artist.__eq__(artist),
                  )
            if low_title.__eq__(org_title) and low_artist.__eq__(artist):
                return music_id
            if low_title.__contains__(org_title):
                if expect_string(low_title, title):
                    return music_id
                elif expect_string(low_title, org_title):
                    return music_id
                if low_title.__eq__(org_title):
                    if low_artist.__contains__(artist):
                        return music_id
                    elif low_artist.__eq__(artist):
                        return music_id
            elif low_title.__eq__(title):
                if low_artist.__contains__(artist):
                    return music_id
                elif low_artist.__eq__(artist):
                    return music_id
                else:
                    continue
            else:
                continue

        if len(music_id_list_acc).__eq__(0):
            music_id = int(music_id_list[0])
        else:
            music_id = int(music_id_list_acc[0])
        return music_id

    def get_music_id_by_title(org_title: str, title: str) -> int or None:
        url = MelonSong_tagUrl + quote(title)
        if check_work(url):
            raise AlreadyExistsError
        pprint(f'{title} : {url}')
        return _get_music_id(url, title, org_title, "")

    def get_music_id_by_title_artist(org_title: str, title: str, artist: str) -> int or None:
        if title is None or title == 'None' or title == '' or len(title) == 0:
            raise search_error
        if artist is None or artist == 'None' or artist == '':
            return get_music_id_by_title(org_title, title)
        url = MelonSong_tagUrl + quote(title) + '+' + quote(artist)
        if check_work(url):
            raise AlreadyExistsError
        pprint(f'{title} + {artist} : {url}')
        return _get_music_id(url, title, org_title, artist)

    def search_title_artist(title, artist):
        try:
            return get_music_id_by_title_artist(title, title, artist)
        except search_error:
            pass
        try:
            return get_music_id_by_title_artist(title, find_text('[가-힣]+', title, True), artist)
        except search_error:
            pass
        try:
            return get_music_id_by_title_artist(title, sub(r'\(.+?\)$', '', title), artist)
        except search_error:
            pass
        try:
            return get_music_id_by_title_artist(title, sub(r'\(*\)*', '', title), artist)
        except search_error:
            raise search_error

    search_error = SearchError

    try:
        return search_title_artist(title, artist)
    except search_error:
        pass
    try:
        return search_title_artist(title, tran_text(artist))
    except search_error:
        pass
    try:
        return search_title_artist(tran_text(sub("[가-힣]", '', title)), artist)
    except search_error:
        pass
    try:
        return get_music_id_by_title(title, title)
    except search_error as error:
        not_working_list(target)
        # raise ValueError(f'{error}: Did not search "{title}, {artist}"') from error
        print(error)


def get_title_artist_mp3(target_mp3: str) -> tuple[str, str]:
    """
    get title and artist in mp3
    :param target_mp3: to get title and artist
    :return: info(title, artist)
    """
    check_type(target_mp3, str)

    audio_tag = eyed3.load(target_mp3).tag
    if (artist := str(audio_tag.artist)) is None or artist == 'None':
        artist = ''
    for i in expect_artist:
        if i in artist:
            artist = artist.replace(i, '')
    # artist = str(artist_name_list.get(artist.strip().lower(), artist))
    for i, j in artist_name_list.items():
        i = i.lower().strip().replace(" ", "")
        j = j.lower().strip().replace(" ", "")
        artist = artist.lower().strip().replace(" ", "")
        print(i, j, artist)
        if artist.__eq__(i):
            artist = j
            break
        # elif artist.__contains__(i) or i.__contains__(artist):
        #     print('event!!')
        #     artist = j
        #     break
        else:
            continue
    else:
        artist = artist  # skip

    if (title := str(audio_tag.title)) is None or title == 'None':
        title = str(audio_tag.album)
    return title, artist


def get_tag(music_id: str or int) -> str or int:
    """
    get tag by music_id
    :param music_id: to get tag music_id
    :return: album_names:str, album_artist:str, title:str,
            album_id:int, year:str, genre:str, lyric:str
    """
    check_type(music_id, (str, int))
    adult_only = '19금'
    soup = get_soup(MelonSongUrl + str(music_id), get_tag.__name__)
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
    soup = soup.select('.lyric')
    try:
        if len(soup) == 0:
            raise IndexError('No lyric')
        soup = soup[0]
        for i in soup.find_all('br'):
            i.replace_with('\n')
        lyric = str(soup.get_text()).replace("\n", "\n\n").strip()
    except IndexError:
        pprint('No lyric')
        lyric = ''
    finally:
        del soup
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
    check_type(album_id, (str, int))
    try:
        url = MelonAlbumUrl + str(album_id)
        soup = get_soup(url, get_album_img.__name__)
    except GetInfoError:
        url = MelonAlbumUrl + str(album_id[:album_id_short])
        soup = get_soup(url, get_album_img.__name__)
    album_img = soup.select('meta[property="og:image"]')[0]
    pprint(f'album : {url}')
    url = find_text('content="(.+?)"', album_img)
    try:
        img = get_img_by_url((url := url.replace('500.jpg', '1000.jpg')))
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
    check_type(title, str)
    check_type(album_id, (str, int))
    try:
        url = MelonAlbumUrl + str(album_id)
        soup = get_soup(url, get_track_num.__name__)
    except GetInfoError:
        url = MelonAlbumUrl + str(album_id[:album_id_short])
        soup = get_soup(url, get_track_num.__name__)
    title_in_album = []
    for i in soup.select('.wrap_song_info'):
        temp_title_in_album = find_text('>(.+?)</a>', i)
        if '&amp;' in temp_title_in_album:
            temp_title_in_album = temp_title_in_album.replace('&amp;', '&')
        # if '(Inst.)' not in temp_title_in_album:
        #     title_in_album.append(temp_title_in_album)
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
