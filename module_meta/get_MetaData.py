import os
import time

from .all_code import get_mp3, start, arr_work


def apply_meta(target: str or list = os.getcwd()):
    """
    apply meta data to mp3 file
    :param target: str or list, explorer address to get meta data
    :return:
    """
    timer = time.time()
    if type(target) is not list:
        if '.mp3' in target:
            arr = [target.replace("\\", "/")]
        else:
            arr = get_mp3(target)
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
    print(f"not work : {arr_work}")
    return

