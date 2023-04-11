# import multiprocessing
import os
import argparse
from get_metadata.b_copy import copy_file, remove_title_artist
from get_metadata.get_MetaData import apply_meta as a1
from get_metadata.get_MetaData_multi import get_meta_multi as a2

# if __name__ == '__main__':
#     multiprocessing.freeze_support()
#     target = os.getcwd() + '/music'
#     a2(target)

# or

if __name__ == '__main__':
    # preser = argparse.ArgumentParser(description='Get MetaData through melon', epilog='Get MetaData through melon')
    # preser.add_argument('-f1', '--F_e', help='paste file',
    #                     required=True, type=str, nargs=1)
    # preser.add_argument('-f2', '--S_e', help='copy file',
    #                     required=True, type=str, nargs=1)
    # args = preser.parse_args()
    # paste_folder = args.F_e[0]
    # target_2 = args.S_e[0]

    target_1 = r"G:\pyecharm\pythonProject\pythonProject\Apply_MetaData\music"
    target_2 = r"F:\ProgramData\Microsoft\NIVDA\hiromi_downloader_GuI__2\hitomi_downloaded_youtube"
    copy_file(target_2, target_1)
    a1(target_1)
    remove_title_artist(target_1)


    # from get_metadata.t import start
    # start()