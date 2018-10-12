import re
from urllib import request
import requests
import time
from scrapy import Selector

def down(url):
    session = requests.Session()
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.44 (Edition B2)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
                 }

    response = session.get(url=url,headers=headers,)
    print(len(response.text))
    song_list = Selector(response).xpath('//ul[@class="f-hide"]/li').extract()
    i = 1
    for item in song_list:
        # print(item)
        song_id = re.compile('\d+').findall(item)[0]
        print(song_id)
        song_name = re.compile('\d+">(.*?)</a>').findall(item)[0]
        print(str(i)+"正在下载："+song_name)
        singer_url = 'http://music.163.com/song/media/outer/url?id=%s.mp3' %song_id
        request.urlretrieve(singer_url, "%s.mp3" %song_name, )
        print('下载完成：'+song_name +str(song_id))
        i += 1
        times = float(str(time.time())[9:12])
        print('------等待------' + str(times))
        time.sleep(times)


if __name__ == '__main__':
    url = 'https://music.163.com/discover/toplist?id=3778678' # 热歌榜
    down(url)
    print('ALL DOWN')