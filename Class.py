import multiprocessing
import os

from module_meta.get_MetaData import apply_meta
from module_meta.get_MetaData_multi import get_meta_multi


class Get_MetaData:

    def __init__(self, address, mode):
        self.address: str = address
        self.mode: int = mode

    @property
    def address(self):
        return self._address  # property 사용해 리턴하는 함수를 변수처럼 만듦

    @address.setter
    def address(self, address):
        if len(os.listdir(address)) < 0:
            raise NotADirectoryError(f'Not found File in {address}')
        else:
            print('pass')
            self._address = address  # 세터를 사용해 self._address 선언

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode

    def start(self):
        if self._mode == 0:
            apply_meta(self._address)
        elif self._mode == 1:
            multiprocessing.freeze_support()
            get_meta_multi(self._address)
        else:
            raise ValueError


if __name__ == '__main__':
    meta = Get_MetaData('G:\pyecharm\pythonProject\pythonProject\Apply_MetaData\music', 0)
    print(meta.address)
    meta.start()

# setter -> property (매개변수값설정 -> 함수를 지역변수처럼 설정)
