import multiprocessing
import os

from module_meta.b_copy import copy_file
from module_meta.get_MetaData import apply_meta as a1
from module_meta.get_MetaData_multi import get_meta_multi as a2

if __name__ == '__main__':
    multiprocessing.freeze_support()
    target = os.getcwd() + '/music'
    a2(target)

# or

if __name__ == '__main__':
    # target = os.getcwd() + '/music'
    target_1 = r"G:\pyecharm\pythonProject\pythonProject\Apply_MetaData\msuic_1\\"
    target_2 = r"F:\ProgramData\Microsoft\NIVDA\hiromi_downloader_GuI__2\hitomi_downloaded_youtube"
    copy_file(target_1, target_2)
    a1(target_1)

