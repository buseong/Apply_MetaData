import os
from time import time
from time import sleep
from .main_code import start
from .utill.utill import get_mp3_address


def apply_meta(target: str or list = os.getcwd()):
    timer = time()
    # arr = map(lambda x: target.replace("\\", "/"), target)
    if not isinstance(target, list):
        if '.mp3' in target:
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
        start(i)
        print(time() - start_time)
        print('-' * 130)
    time_er = time() - timer
    print(f'Total : {time_er}')
    if n != 0:
        print(f'Avg__ : {time_er / n}')
    # print(f"not work : {arr_work}")
