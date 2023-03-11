import re
from os import path, listdir
from os.path import isdir
from random import randint
from urllib import request
from time import time
import psutil
from bs4 import BeautifulSoup
from googletrans import Translator

from ..Data import headers, expect_title


start_time = time()


def time_count(reformat='10.6'):
    return f'{time() - start_time: {reformat}f}'


def get_soup(url: str, usage: str = ""):
    """
    get soup
    :param url: to get soup
    :param usage: to record where this function was executed
    :return: soup
    """
    check_type(url, str)
    check_type(usage, str)
    pprint(f'{usage} : {url}')
    opener = request.build_opener()
    header = headers[randint(0, len(headers) - 1)]
    opener.addheaders = header
    request.install_opener(opener)
    with request.urlopen(url) as html:
        soup = BeautifulSoup(html.read(), "html.parser")
    return soup


def check_type(target, type_: tuple[bool] or bool):
    """
    check argument-instance - type
    :param target: to chek argument-instance
    :param type_: type
    """

    def check_type(target, type_):
        return isinstance(target, type_)

    def check(target, type_):
        if isinstance(target, tuple):
            if isinstance(type_, tuple):
                return all([check_type(i, type_) for i in target])
            return all([check_type(i, type_) for i in target])
        if isinstance(type_, tuple):
            return any([check_type(target, i) for i in type_])
        return check_type(target, type_)
    if isinstance(type_, tuple):
        msg = ' and '.join([i.__name__ for i in type_])
    else:
        msg = type_.__name__
    assert check(target, type_), TypeError(f'"{target}" is not {msg}')
    return True


class pprint(object):
    def __init__(self, msg=None, types: bool = True, reformat: str = '10.6'):
        if msg is not None:
            if types:
                memory_info = psutil.Process().memory_info()
                rss = memory_info.rss / 2 ** 20
                vms = memory_info.vms / 2 ** 20
                print(f"{time_count()}| RSS: {rss: {reformat}f} MB, VMS: {vms: {reformat}f} | {msg}")
        else:
            pass

    @staticmethod
    def line(text='-', num: int = 130):
        print(str(text)*num)


def spilt_text(text: str, spilt_t: str) -> list:
    """
    spilt text
    :param text: text to divide
    :param spilt_t: to divide the text into
    :return: text
    """
    return text.split(spilt_t)


def remove_text(text: str):
    """
    remove text in text-instance
    :param text: to remove text
    :return: text
    """
    check_type(text, str)
    text_r = ''
    for i in expect_title:
        if i in text:
            text_r = text.replace(i, '')
            text = text_r
        else:
            text_r = text
    return text_r


def tran_text(text: str, spilt_t: str = '+') -> str:
    """
    translation text
    :param text: to translation text
    :param spilt_t:
    :return:
    """
    check_type(text, str)
    check_type(spilt_t, str)
    if spilt_t in text:
        result = ' + '.join(tran_text(remove_text(i).strip()) for i in spilt_text(text, spilt_t))
    else:
        result = str(Translator().translate(text, src='en', dest='ko').text).strip()
    return result


def find_text(pattern: str, text: str, all_str=False) -> str:
    """
    find text by pattern
    :param pattern: to get text pattern
    :param text: text
    :param all_str: default is return first-list-index but all_str is True: return all list-index
    :return: found text
    """

    if not isinstance(text, str):
        text = str(text)
    try:
        find_text_value = re.findall(pattern, text)
        if all_str:
            find_text_value = ' '.join(find_text_value)
        else:
            find_text_value = str(find_text_value[0])
    except IndexError:
        find_text_value = ''
    return find_text_value


def get_img_by_url(url: str) -> bytes:
    """
    get img by url_img-instance
    :param url: to get img url
    :return: img
    """
    check_type(url, str)
    try:
        with request.urlopen(url) as img:
            img = img.read()
    except RuntimeError:
        img = b''
    return img


def get_mp3_address(target: str) -> list:
    """
    get address-mp3-file
    :param target: to get explorer-address
    :return: list-mp3-file
    """
    check_type(target, str)
    folder = target.replace("\\", "/")
    assert isdir(folder), FileNotFoundError(f'"{folder}"-folder not found')
    folder += '/'

    now_file_edit = [folder + i for i in listdir(folder) if path.splitext(i)[1] == '.mp3']
    return now_file_edit
