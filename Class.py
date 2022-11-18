import os

from module_meta.get_data import get_metadata


class Get_Metadata:

    def __init__(self, target='', mode=0, log=False):
        self.target = target
        self.mode = mode
        self.log = log
        self.music_id = None
        self.title = None
        self.artist = None
        self.albumName = None
        self.albumYear = None
        self.albumGenre = None
        self.musicLyric = None
        self.albumId = None
        self.track_num = None
        self.albumImg = None

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        if not isinstance(target, str):
            raise TypeError(...)
        else:
            self._target = target

    @property
    def mode(self):
        if self._mode == 0:
            return 'single'
        elif self._mode == 1:
            return 'multi'
        else:
            return f'Value Error Try Again, mode={self._mode}'

    @mode.setter
    def mode(self, mode):
        if isinstance(mode, str):
            if mode == 'single':
                self._mode = 0
            elif mode == 'multi':
                self._mode = 1
        elif isinstance(mode, int):
            if mode == 0 or 1:
                self._mode = mode
        else:
            raise ValueError(...)

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, log):
        if not isinstance(log, bool):
            raise TypeError(f"'{log}' is not bool")
        else:
            self._log = log

    def get_tag(self, target=...):
        if target is ...:
            target = self._target
        self.pprint(target)
        if target == '':
            raise ValueError
        elif not os.path.isfile(target):
            raise FileNotFoundError

        self.music_id, \
            self.artist, \
            self.title, \
            self.albumName, \
            self.albumYear, \
            self.albumGenre, \
            self.musicLyric, \
            self.albumImg, \
            self.track_num, \
            self.albumId = \
            get_metadata(target, self.log)
        self.pprint(self.music_id,
                    self.artist,
                    self.title,
                    self.albumName,
                    self.albumYear,
                    self.albumGenre,
                    self.track_num,
                    self.albumId,
                    self.musicLyric
                    )

    def save_tag(self):
        eyed3.log.setLevel("ERROR")
        audio_file = eyed3.load(target)
        if not audio_file.tag:
            audio_file.initTag()
        audio_file.tag.title = self.title
        audio_file.tag.album_artist = self.artist
        audio_file.tag.album = self.albumName
        audio_file.tag.track_num = self.trackNum
        audio_file.tag.genre = self.albumGenre
        audio_file.tag.artist = self.artist
        audio_file.tag.recording_date = self.albumYear
        audio_file.tag.lyrics.set(self.musicLyric)
        audio_file.tag.images.set(ImageFrame.FRONT_COVER, self.albumImg, 'image/jpeg')
        audio_file.tag.save(encoding='utf-8')

    def pprint(self, *args):
        if self.log:
            if len(args) == 1:
                print(args[0])
            else:
                for i in args:
                    print(i, end=' | ')
        else:
            pass


if __name__ == '__main__':
    gt = Get_Metadata(target='', mode=0, log=False)
    gt.get_tag()
    print(gt.__dict__)
