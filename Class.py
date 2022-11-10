import multiprocessing
import os

from module_meta.get_MetaData import apply_meta
from module_meta.get_MetaData_multi import get_meta_multi


class Get_MetaData:

    def __init__(self, address, mode=0):
        self.address: str = address
        self.mode: int = mode

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        if not isinstance(address, str):
            raise ValueError(f'{address} is not correct value type')
        else:
            if len(os.listdir(address)) < 0:
                raise NotADirectoryError(f'Not found File in {address}')
            else:
                print('pass')
                self._address = address

    @property
    def mode(self):
        mode = self._mode
        if mode == 0:
            return 'single core'
        elif mode == 1:
            return 'multi core'

    @mode.setter
    def mode(self, mode):
        if isinstance(mode, int):
            if mode == 0:
                self._mode = mode
            elif mode == 1:
                self._mode = mode
        elif isinstance(mode, str):
            if mode == 'single':
                self._mode = 0
            elif mode == 'multi':
                self._mode = 1
        else:
            raise ValueError(f'{mode} is not correct value type or value')

    def start(self):
        if self._mode == 0:
            apply_meta(self._address)
        elif self._mode == 1:
            multiprocessing.freeze_support()
            get_meta_multi(self._address)
        else:
            raise RuntimeError('Something was wrong, please try late')


if __name__ == '__main__':
    meta = Get_MetaData('G:\pyecharm\pythonProject\pythonProject\Apply_MetaData\music', 0)
    print(meta.address)
    meta.start()

# setter -> property (매개변수값설정 -> 함수를 지역변수처럼 설정)
