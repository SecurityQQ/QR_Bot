import requests as r
import re
import json

AVAILABLE_FORMATS = ['png', 'jpg', 'jpeg', 'bmp']

def get_images_urls(name):
    s = r.get("https://api.cognitive.microsoft.com/bing/v7.0/images/search/?q={}".format(name),
              headers={"Ocp-Apim-Subscription-Key": "63b3ee16a46847e0be92920dd1409024"})

    content = json.loads(s.content).get('value')
    return list(map(lambda x: x.get('contentUrl'), content))


def is_url(url):
    pattern = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return len(re.findall(pattern, url)) == 1


def download_image(url):
    if url is None:
        return None
    req = r.get(url)
    if req.status_code != 200:
        return None
    else:
        try:
            content = req.content.decode('utf-8')
        except UnicodeDecodeError:
            content = req.content
        return content

def is_supporting_format(url):
    return url[-3:] in AVAILABLE_FORMATS or url[-4] == 'jpeg'


def smart_choice(urls):
    filtered_urls = list(filter(is_url, urls))
    filtered_urls = list(filter(is_supporting_format, filtered_urls))
    if len(filtered_urls) == 0:
        return None
    return filtered_urls[0]


def get_smart_image(name):
    extention = name.split('.')[-1]

    if extention not in AVAILABLE_FORMATS:
        extention = 'png'
        name = name + ' .' + extention

    if 'icon' not in name:
        name = name + ' icon'

    urls = get_images_urls(name)
    best_url = smart_choice(urls)
    print(best_url)
    return download_image(best_url)
