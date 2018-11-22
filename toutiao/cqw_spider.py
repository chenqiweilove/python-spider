import os
import re
import time
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from requests.exceptions import RequestException
from hashlib import md5
def get_page_index(offset, keyword):

    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': 3,
        'from': 'gallery'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return  None
    except RequestException:
        print("请求索引页出错")
        return  None

def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3325.181',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return  None
    except RequestException:
        print("请求详情页出错")
        return  None

def parse_page_detail(html, url):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('title')[0].get_text()
    images_pattern = re.compile('JSON.parse\("(.*?)"\),', re.S)
    result = re.search(images_pattern, html)
    if result:
        data = json.loads(result.group(1).replace('\\',''))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images: download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def download_image(url):
    print('正在下载', url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3325.181',
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            save_image(response.content)
        return  None
    except RequestException:
        print("请求图片出错")
        return  None

def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

def main():
    html = get_page_index(0, '街拍')
    # print(html) ##索引页html信息
    for url in parse_page_index(html):#分析索引页，提取详情页url
        time.sleep(10)
        print('2------------------2')
        print(url)
        html = get_page_detail(url) #详情页html信息
        print('3---------------------3')
        print(html)
        if html:
            result = parse_page_detail(html, url)
            print('4-------------------4')
            print(result)
            print('---------------end--------------------')
            print('\n')


if __name__ == '__main__':
    main()