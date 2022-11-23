"""
Made By Buseong
"""
import os
import re
import shutil

import eyed3

from .main_code import get_mp3_address


def copy_file(target_1, target):
    """
    copy file-mp3 in target_1-argument to target-argument
    :param target_1: to copy directory
    :param target: to paste directory
    """
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


def remove_bracket(text: str) -> str:
    """
    remove bracket in text
    :param text: to remove text
    :return: removed text
    """
    if not isinstance(text, str):
        text = str(text)
    text = re.sub('\\([^)]*\\)+', '', text)
    return text


def remove_title_artist(target):
    """
    remove bracket in title, artist, album_artist
    :param target: to remove title, artist, album_artist
    """
    for i in get_mp3_address(target):
        audio_tag = eyed3.load(i).tag
        audio_tag.artist = remove_bracket(audio_tag.artist)
        audio_tag.album_artist = remove_bracket(audio_tag.album_artist)
        audio_tag.title = remove_bracket(audio_tag.title)
        audio_tag.album = remove_bracket(audio_tag.album)
        audio_tag.save(encoding='utf-8')
