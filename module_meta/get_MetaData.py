import os
import time

from .main_code import get_mp3_address, start


def apply_meta(target: str or list = os.getcwd()):
    timer = time.time()
    if not isinstance(target, list):
        if '.mp3' in target:
            arr = [target.replace("\\", "/")]
        else:
            arr = get_mp3_address(target)
    else:
        arr = target
    if len(arr) < 0:
        raise ValueError(f'Not found file in {arr}')
    for i in arr:
        start_time = time.time()
        start(i)
        print(time.time() - start_time)
        print('-' * 130)
    time_er = time.time() - timer
    print(f'Total : {time_er}')
    print(f'Avg__ : {time_er / len(arr)}')
    # print(f"not work : {arr_work}")
    return

