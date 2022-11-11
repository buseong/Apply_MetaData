artist_name_list: dict[str, str] = {
        'LOONA': '이달의 소녀',
        'SUNMI': '선미',
        'JOY': '조이',
        'CHUNG HA': '청하',
        '(G)I-DLE': '(여자)아이들',
        'YUQI ((G)I-DLE)': '우기 ((여자)아이들)',
        'TAEYEON': '태연',
        'fromis_9': '프로미스나인',
        'JO YURI': '조유리',
        'fromis9': '프로미스나인',
        'Various Artists': '',
        'IU': '아이유',
        'JEON SOMI': '전소미',
        'Baek A-yeon': '백아연',
        'WJSN': '우주소녀',
        'Orange Caramel': '오렌지 캬라멜',
        'Ulala Session':  '울랄라세션',
        'LOVELYZ': '러블리즈',
        'Solar Ft. Justo': '솔라',
        'Whee In': '휘인',
        'Younha': '윤하',
        'Moonbyul': '문별',
        'Davich': '다비치',
        'MAKTUB': '마크툽',
        'Jang Beom June': '장범준',
        'J-Cera': '제이세라',
        'MoonMoon': '문문',
        'Jung Dong Ha': '정동하',
        'Yerin Baek': '백예린',
        'MeloMance':  '멜로망스',
        'Standing Egg': '스탠딩 에그',
        'Loco': '로꼬',
        'Motte': '모트',
        'VIBE': '바이브',
        'Lim Jae Hyun': '임재현',
        'BOL4': '볼빨간사춘기',
        'Noel': '노을',
        'GyeongseoYej': '경서예지',
        'Homies': '호미들',

    }

headers: list[list[(str, str)]] = [
               [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36')],
               [('User-Agent', '"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"')],
               [('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36')],
               [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0')],
               [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ')],
               [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ')],
               ]

key_list: list[str] = ['title', 'album', 'track_num', 'artist', 'album_artist', 'recording_date', 'genre', 'lyrics', 'image']

music_id_l: int = 4
album_list_l: int = 3
album_id_short: int = 7

MelonAlbumUrl: str = "https://www.melon.com/album/detail.htm?albumId="
MelonSongUrl: str = "https://www.melon.com/song/detail.htm?songId="
MelonSong_tagUrl: str = "https://www.melon.com/search/song/index.htm?q="
