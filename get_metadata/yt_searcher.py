from urllib.parse import quote

import yt_dlp
from selenium import webdriver
from selenium.webdriver.common.by import By

from get_melon_chart import get_chart
from main_code import *


def get_search_result(title, artist):
    url = 'https://www.youtube.com/results?search_query=' + quote(f'{title} {artist} official audio')
    print(url)
    driver = webdriver.Chrome(executable_path='chromedriver.exe')
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
    download_yt(get_search_result(title, artist)[num], target)


def get_set_tag(music_id, target):
    album_name, album_artist, title, album_id, year, genre, lyric = get_tag(music_id)
    img, track_num = get_album_img(album_id)
    save_tag(
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
    title, artist, music_id = get_chart(0)
    target = os.getcwd() + '\\' + f'{title}.mp3'
    get_music(title, artist, target)
    get_set_tag(music_id, target)

