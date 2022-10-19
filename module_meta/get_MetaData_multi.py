import multiprocessing
import os
import time

from .all_code import get_mp3, start, arr_work


def apply_meta(target):
    """
    apply meta data to mp3 file
    :param target: str or list, explorer address to get meta data
    # :param mode: int, user select mode
    :return:
    """
    timer = time.time()
    arr = [target]
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


def check_meta(target):
    audio_file = eyed3.load(target)
    return (
            audio_file.tag.album_artist,
            audio_file.tag.title,
            audio_file.tag.album,
            audio_file.tag.genre,
            audio_file.tag.artist,
            audio_file.tag.recording_date,
            audio_file.tag.track_num,
            audio_file.tag.lyrics
            )


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
    """
    start work multi-processing
    :param target: explorer address
    :param num: cpu thread num
    :return:
    """
    start_time = time.time()
    arr = get_mp3(target)
    if len(arr) < num:
        raise ValueError(f'file num {len(arr)} > cpu num {num}')
    brr = sort_num(arr, num)
    pool = multiprocessing.Pool(processes=num)
    for i in range(int(num)):
        pool.map(apply_meta, brr[i])
    pool.close()
    pool.join()
    print('='*90)
    print(time.time() - start_time)
    return
