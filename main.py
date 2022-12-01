"""
Made By Buseong
"""
import os

import eyed3
import psutil
from eyed3.id3.frames import ImageFrame

from get_metadata.main_code import start
from get_metadata.Data import tag_list


class GetMetaDataBase(object):
    """
    get metadata by title and artist in mp3-file
    """

    def __init__(self,
                 target: str,
                 log: bool = False
                 ):
        self.target = target
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

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, log):
        if not isinstance(log, bool):
            raise TypeError(f"'{log}' is not bool")
        self._log = log

    def get_tag(self, target=None):
        if target is None:
            target = self._target
        self.pprint(target)
        if target == '':
            raise ValueError
        if self.target == '':
            raise ValueError
        if not os.path.isfile(target):
            raise FileNotFoundError(f'"{target}" - file is not found')
        if os.path.splitext(target)[1] != '.mp3':
            raise FileNotFoundError(f'{target} is not mp3-file')
        metadata_info = start(target, return_type=True)  # bt Data.tag_list
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
        if self._log:
            if len(args) == 1:
                print(args[0])
            else:
                for i in args:
                    print(i, end=' | ')


class GetMetaData(GetMetaDataBase):
    def __init__(self, target: str, log: bool = False):
        super(GetMetaData, self).__init__(target=target, log=log)
        self.meta_info = None

    def get_tag(self, target=None):
        if target is None:
            if self._target is None:
                raise ValueError(f'"{target} amd {self._target} is empty')
            target = self._target
        if not os.path.isfile(target):
            raise FileNotFoundError(f'"{target}" - file is not found')
        if os.path.splitext(target)[1] != '.mp3':
            raise FileNotFoundError(f'{target} is not mp3-file')
        self.meta_info = start(target, return_type=True)  # by Data.tag_list
        for i in tag_list:
            setattr(self, i, self.meta_info[i])

    def save_tag(self):
        eyed3.log.setLevel("ERROR")
        audio_file = eyed3.load(self.target)
        if not audio_file.tag:
            audio_file.initTag()
        for key, value in self.meta_info.items():
            if key in tag_list:
                if key == 'lyrics':
                    audio_file.tag.lyrics.set(value)
                elif key == 'track_num':
                    audio_file.tag.track_num = value
                elif key == 'image':
                    audio_file.tag.images.set(ImageFrame.FRONT_COVER, value, 'image/jpeg')
                else:
                    setattr(audio_file.tag, key, value)
            else:
                pprint(f'{key} is not in {tag_list}')
        audio_file.tag.save(encoding='utf-8')


if __name__ == '__main__':
    target = r'G:\pyecharm\pythonProject\pythonProject\Apply_MetaData\music\Tick Tick Boom (Tick Tick Boom).mp3'
    gt = GetMetaData(target)
    gt.get_tag()
    print(gt.artist)
