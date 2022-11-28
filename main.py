"""
Made By Buseong
"""
import os

import eyed3
import psutil
from eyed3.id3.frames import ImageFrame

from get_metadata.main_code import start
from get_metadata.Data import key_list


class GetMetaDataBase(object):
    """
    get metadata by title, artist in mp3-file
    """

    def __init__(self,
                 target: str,
                 # mode: int = 0,
                 log: bool = False
                 ):
        self.target = target
        # self.mode = mode
        self.log = log
        self.title = None
        self.artist = None
        self.album_name = None
        self.album_year = None
        self.album_genre = None
        self.music_lyric = None
        self.track_num = None
        self.album_img = None

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        if not isinstance(target, str):
            raise TypeError(f'"{target}" is not str')
        self._target = target

    # @property
    # def mode(self):
    #     if self._mode == 0:
    #         return 'single'
    #     if self._mode == 1:
    #         return 'multi'
    #     return f'Value Error Try Again, mode={self._mode}'
    #
    # @mode.setter
    # def mode(self, mode):
    #     if isinstance(mode, str):
    #         if mode == 'single':
    #             self._mode = 0
    #         elif mode == 'multi':
    #             self._mode = 1
    #     elif isinstance(mode, int):
    #         if mode == 0 or 1:
    #             pass
    #     else:
    #         raise ValueError(...)

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, log):
        if not isinstance(log, bool):
            raise TypeError(f"'{log}' is not bool")
        self._log = log

    def get_tag(self, target=...):
        if target is ...:
            target = self._target
        self.pprint(target)
        if target == '':
            raise ValueError
        if self.target == '':
            raise ValueError
        if not os.path.isfile(target):
            raise FileNotFoundError(f'"{target}" - file is not found')
        if not os.path.splitext(target)[1] == '.mp3':
            raise FileNotFoundError(f'{target} is not mp3-file')

        metadata_info = start(target, return_type=True)  # bt Data.key_list
        self.album_name = metadata_info['album']
        self.artist = metadata_info['album_artist']
        self.title = metadata_info['title']
        self.album_img = metadata_info['image']
        self.album_genre = metadata_info['genre']
        self.album_year = metadata_info['recording_date']
        self.music_lyric = metadata_info['lyrics']
        self.track_num = metadata_info['track_num']

        self.pprint(
                    self.artist,
                    self.title,
                    self.album_name,
                    self.album_year,
                    self.album_genre,
                    self.track_num,
                    self.music_lyric
                    )

    def save_tag(self):
        eyed3.log.setLevel("ERROR")
        audio_file = eyed3.load(self._target)
        if not audio_file.tag:
            audio_file.initTag()
        audio_file.tag.title = self.title
        audio_file.tag.album_artist = self.artist
        audio_file.tag.album = self.album_name
        audio_file.tag.track_num = self.track_num
        audio_file.tag.genre = self.album_genre
        audio_file.tag.artist = self.artist
        audio_file.tag.recording_date = self.album_year
        audio_file.tag.lyrics.set(self.music_lyric)
        audio_file.tag.images.set(ImageFrame.FRONT_COVER, self.album_img, 'image/jpeg')
        audio_file.tag.save(encoding='utf-8')

    def pprint(self, *args):
        """
        print args
        :param args: to print text: tuple
        """
        if self.log:
            if len(args) == 1:
                print(args[0])
            else:
                for i in args:
                    print(i, end=' | ')


class GetMetaData(GetMetaDataBase):
    pass


if __name__ == '__main__':
    target = r'G:\pyecharm\pythonProject\pythonProject\Apply_MetaData\music\Tick Tick Boom (Tick Tick Boom).mp3'
    gt = GetMetaData(target)
    gt.get_tag()
    print(gt.title)
