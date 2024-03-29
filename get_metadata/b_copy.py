"""
Made By Buseong
"""
import os
import re
import shutil
import eyed3

from .utill.utill import get_mp3_address


def copy_file(copy_folder: str, paste_folder: str, extension: str = 'mp3'):
    """
    copy file-mp3 in target_1-argument to target-argument
    :param paste_folder: to paste directory
    :param copy_folder: to copy directory
    :param extension: to copy file-extension
    """

    def address_format(address: str) -> str:
        if address[-1] != '\\' or '/':
            address += '/'
        address = address.replace('\\', '/')
        return address

    if extension[0] != '.':
        extension = '.' + extension

    copy_folder = address_format(copy_folder)
    paste_folder = address_format(paste_folder)

    file_in_folder = []
    file_in_folder_address = []

    for i in os.listdir(copy_folder):
        if os.path.splitext(i)[1] == extension:
            file_in_folder.append(copy_folder + i)
            file_in_folder_address.append(os.path.splitext(i)[0] + extension)
    for j, _ in enumerate(file_in_folder_address):
        shutil.copy(file_in_folder[j], paste_folder + file_in_folder_address[j])


def remove_title_artist(target):
    """
    remove bracket in title, artist, album_artist
    :param target: to remove title, artist, album_artist
    """

    def remove_bracket(text: str) -> str:
        """
        remove bracket in text
        :param text: to remove text
        :return: removed text
        """
        if not isinstance(text, str):
            text = str(text)
        text = re.sub(r'\(.+?\)$', '', text)
        return text

    tag_list = ['album_artist', 'title', 'album', 'artist']
    for i in get_mp3_address(target):
        audio_tag = eyed3.load(i).tag
        for j in tag_list:
            setattr(audio_tag, j, remove_bracket(getattr(audio_tag, j)))
        audio_tag.save(encoding='utf-8')
