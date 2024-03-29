__all__ = ['artist_name_list', 'headers', 'tag_list', 'expect_artist', 'expect_title', 'album_id_short',
           'MelonSongUrl', 'MelonSong_tagUrl', 'MelonAlbumUrl'
          ]

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
        'V/A': '',
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
        "BE'O": '비오',
        'lIlBOI': '릴보이',
        'JUSTHIS': '저스디스',
        'DPR LIVE': '디피얼 라이브',
        'Dreamcatcher': '드림캐쳐',
        'Kim Ye-ji': '김예지',
        'Shin Youme': '신유미',
        'Chuu': '츄',
        'KWON EUN BI': '권은비',
        'KARA': '카라',
        'Tophyun': '탑현',
        'Seo In Guk': '서인국',
        'Heize': '헤이즈',
        'Yoon Mi-rae': '윤미래',
        'meenoi': '미노이',
        'K.Will': '케이윌',
        'Lee Young Ji': '이영지',
        'So Soo Bin': '소수빈',
        'SeeYa': '씨야',
        'EPIK HIGH': '에픽하이',
        'Kim Dong-ryul': '김동율',
        'Naul': '나얼',
        'Sunny Hill': '써니휠',
        'M.C the MAX': '엠씨더맥스',
        'OH MY GIRL': '오마이걸',
        'WSG WANNABE(4FIRE)': 'WSG워너비(4FIRE)',
        'After School': '애프터스쿨',
        'COOING': '쿠잉',
        'Kim Kyung-ho': '김경호',
        'ZIA': '지아',
        '자두': '더 자두',
        'The Jadu': '더 자두',
        'SG Wannabe': 'SG 워너비',
        'miss A': '미쓰에이',
        'lee hi': '이하이',
        'dosii': '도시',
        'BoA': '보아',
        'Girls` Generation': '소녀시대',
        'U SUNG EUN': '유성은',
        'Seoul Philharmonic Orchestra': '서울시립교향악단',
        'SEVENTEEN': '세븐틴',
        'Secret': '시크릿',
        'SISTAR': '씨스타',
        'T-ara': '티아라',
        'Hyolyn': '효린',
        'Trouble Maker': '트러블메이커',
        'gain': '가인',
        'j.y.park': '박진영',
        'ovan': '오반',
        'pentagon': '펜타곤',
        'leesun-hee': '이선희',
        'leejiyong': 'Various Artists',
        'onestar': '임한별',
        'rumblefish': '럼블피쉬',
        

    }  # 데이터셋을 못찾겠음..

headers: list[list[(str, str)]] = [
               [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36')],
               [('User-Agent', '"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"')],
               [('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36')],
               [('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0')],
               [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ')],
               [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ')],
               ]

tag_list: list[str] = ['title', 'album', 'track_num', 'artist', 'album_artist', 'recording_date', 'genre', 'lyrics', 'image']

# expect_title: list[str] = ['’', '(remix)', '(Remix)', ' - 페이지 이동']
expect_title: list[str] = [' - 페이지 이동']
expect_artist: list[str] = [' - Topic', 'OFFICIAL', 'VEVO']

album_id_short: int = 7

MelonAlbumUrl: str = "https://www.melon.com/album/detail.htm?albumId="
MelonSongUrl: str = "https://www.melon.com/song/detail.htm?songId="
MelonSong_tagUrl: str = "https://www.melon.com/search/song/index.htm?q="
