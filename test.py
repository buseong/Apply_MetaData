import multiprocessing
import os

from module_meta.get_MetaData import apply_meta as a1
from module_meta.get_MetaData_multi import get_meta_multi as a2
from module_meta.b_copy import ht_cp
# if __name__ == '__main__':
#     multiprocessing.freeze_support()
#     target = os.getcwd() + '/music'
#     a2(target)

# or

if __name__ == '__main__':
    # target = os.getcwd() + '/music'
    target = r"G:\pyecharm\pythonProject\pythonProject\Apply_MetaData\msuic_1"
    ht_cp()
    a1(target)

