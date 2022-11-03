import os
import re
import shutil

import eyed3

from .main_code import get_mp3_address


def copy_file(target_1, target):
    folder = target.replace("\\", "/") + '/'
    now_file_edit = []
    name_list = []
    for i in os.listdir(folder):
        if os.path.splitext(i)[1] == '.mp3':
            now_file_edit.append(folder + i)
            name_list.append(os.path.splitext(i)[0] + '.mp3')
    for j in enumerate(name_list):
        j = j[0]
        shutil.copy(now_file_edit[j], target_1 + name_list[j])
    return


def remove_rhksgh(text):
    text = re.sub('\\([^)]*\\)+', '', text)
    return text


def remove_title_artist(target):
    for i in get_mp3_address(target):
        audio_tag = eyed3.load(i).tag
        audio_tag.artist = remove_rhksgh(audio_tag.artist)
        audio_tag.album_artist = remove_rhksgh(audio_tag.album_artist)
        audio_tag.title = remove_rhksgh(audio_tag.title)
        audio_tag.album = remove_rhksgh(audio_tag.album)
        audio_tag.save(encoding='utf-8')
    return
