from urllib.parse import urlencode
import requests
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import re
import pymongo
import os
from hashlib import md5
from multiprocessing import Pool
from json.decoder import JSONDecodeError

group_start = 1
group_end = 20

keyword = "街拍"

mongocli = pymongo.MongoClient(host = "127.0.0.1", port = 27017)
dbname = mongocli["taotiao"]
sheetname = dbname["jiepai"]

def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'gallery'
    }
    url = "https://www.toutiao.com/search_content/?" + urlencode(data)

    try:
        response =requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求索引页出错")
        return None

def parse_page_index(html):
    try:
        data = json.loads(html)
        if data and 'data' in data.keys():
            for item in data.get('data'):
                yield item.get('article_url')
    except JSONDecodeError:
        pass

def get_page_detail(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }
    try:
        response =requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求详情页出错")
        return None

#  解析详情页
def parse_page_detail(html, url):
    soup = BeautifulSoup(html, "lxml")
    title = soup.select('title')[0].text
    images_pattern = re.compile('gallery: JSON.parse.?(.*?).?,\n    siblingList:', re.S)

    result = re.search(images_pattern, html)
    if result:
        data = json.loads(json.loads(result.group(1)))     # 此处提取规则会经常变化
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images: download_image(image)
            return {
                "title": title,
                "url": url,
                "images": images,
            }

#  存储到MONGODB
def save_to_mongo(result):
    if sheetname.insert(result):
        print('存储到MongoDB成功', result)
        return True
    return False

def download_image(url):
    print("正在下载", url )
    try:
        response =requests.get(url)
        if response.status_code == 200:
            save_images(response.content)
            return response.text
        return None
    except RequestException:
        print("请求图片页出错", url)
        return None


# 图片保存至本地
def save_images(content):
    # 使用md5的方式来重命名可以防重复，内容相同md5值相同
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

def main(offest):
    html = get_page_index(offest, keyword)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            if result: save_to_mongo(result)

if __name__ == '__main__':
    groups = [x*20 for x in range(group_start, group_end+1)]
    pool = Pool(processes=4)
    
    for i in range(group_start, group_end+1):
        groups = i*20
        pool.apply_async(main(0), (groups,))
    pool.close()
    pool.join()



