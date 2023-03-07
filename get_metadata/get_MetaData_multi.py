import multiprocessing
import os
from time import time
from .utill.utill import *
from .main_code import start
from .utill.utill import get_mp3_address


def apply_meta(target):
    timer = time()
    arr = [target]
    for i in arr:
        start_time = time()
        start(i)
        print(time() - start_time)
        print('-' * 130)
    time_er = time() - timer
    print(f'Total : {time_er}')
    print(f'Avg__ : {time_er / len(arr)}')


def sort_num(arr_, num):
    k = len(arr_) // num
    el = len(arr_) % num
    arr = [[], ]
    count = 0
    last = 1
    for ch_nam in range(k * num):
        if ch_nam == (k * last):
            arr.append([], )
            count += 1
            last += 1
        arr[count].append(arr_[ch_nam])
    for el_ch in range(el):
        k = len(arr_) - el_ch - 1
        arr[num - 1].append(arr_[k])
    return arr


def get_meta_multi(target: str = os.getcwd(), num: int = multiprocessing.cpu_count()):
    if not isinstance(target, str):
        raise ValueError(f'{target} is not string, {type(target)}')
    start_time = time()
    arr = get_mp3_address(target)
    if (n := len(arr)) < num:
        raise ValueError(f'file num {n} > cpu num {num}')
    brr = sort_num(arr, num)
    pool = multiprocessing.Pool(processes=num)
    for i in range(int(num)):
        pool.map(apply_meta, brr[i])
    pool.close()
    pool.join()
    pprint.line()
