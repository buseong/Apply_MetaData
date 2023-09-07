import os
from time import time
from time import sleep
from .main_code import start
from .utill.utill import get_mp3_address


def apply_meta(target: str or list = os.getcwd(), extension: str = 'mp3', melon_id: int = -1):
    timer = time()
    # arr = map(lambda x: target.replace("\\", "/"), target)
    if extension[0] != ".":
        extension = "." + extension
    if not isinstance(target, list):
        if extension in target:
            arr = [target.replace("\\", "/")]
        else:
            arr = get_mp3_address(target)
    else:
        if not isinstance(target, str):
            raise TypeError(f'{target} is not str or list')
        arr = target
    if (n := len(arr)) < 0:
        raise NotADirectoryError or FileNotFoundError(f'Not found file in {arr}')
    for i in arr:
        start_time = time()
        start(i, melon_id=melon_id)
        print(time() - start_time)
        print('-' * 130)
    time_er = time() - timer
    print(f'Total : {time_er}')
    if n != 0:
        print(f'Avg__ : {time_er / n}')
    # print(f"not work : {arr_work}")
