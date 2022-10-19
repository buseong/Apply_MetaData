import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from all_code import *
from get_melon_chart import get_chart


def get_search_result(title, artist):
    service = Service(ChromeDriverManager().install())
    url = 'https://www.youtube.com/results?search_query=' + urllib.parse.quote(f'{title} {artist} official audio')
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    f_video = driver.find_elements(By.ID, 'video-title')
    video_list = [i.get_attribute('href') for i in f_video if i.get_attribute('href') is not None]
    driver.quit()
    return video_list


def download_yt(url, target):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': target.replace('mp3', 'mp4'),
        'postprocessors':
            [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def get_music(title, artist, target, num=0):
    print(target)
    download_yt(get_search_result(title, artist)[num], target)


def save_tag_(target, **kwargs):
    """
    Save tag to mpeg-3
    :param target: to save mpeg-3 file
    :param kwargs: title, album, recording_date, album_artist, genre, track_num, artist, lyrics, image
    :return:
    """
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
    audio_file.tag.save(encoding='utf-8')
    return


def get_set_tag(music_id, target):
    album_name, album_artist, title, album_id, year, genre, lyric = get_tag(music_id, target)
    img, track_num = get_image_track(album_id, title)
    save_tag_(
        album=album_name,
        album_artist=album_artist,
        title=title,
        image=img,
        target=target,
        genre=genre,
        recording_date=year,
        lyrics=lyric,
        track_num=track_num,
        artist=album_artist
    )


if __name__ == '__main__':
    title, artist, music_id = get_chart(1)
    target = os.getcwd() + '\\' + f'{title}.mp3'
    get_music(title, artist, target)
    get_set_tag(music_id, target)

