from qrcode.MyQR import myqr


import requests as r
import random
import os


def smart_qr_code_by_name(content, seed, suffix=".png", save_name=None, hook=lambda x: x):
    if save_name is None:
        save_name = seed + str(random.randint(1, 100000)) + suffix

    if 'icon' not in seed:
        seed = seed + ' icon' + ' ' + suffix

    name = seed

    print("name: ", name)

    s = r.get("https://api.cognitive.microsoft.com/bing/v7.0/images/search/?q={}".format(name),
              headers={"Ocp-Apim-Subscription-Key": "63b3ee16a46847e0be92920dd1409024"})

    from pprint import pprint
    import json

    url = json.loads(s.content.decode('utf8')).get('value')[0].get('contentUrl')

    print('url: ', url)
    import tempfile
    with open("tmp"+suffix, 'wb+') as fp:
        fp.write(r.get(url).content)
        path = fp.name
        print(path)
        try:
            ver, ecl, qr_name = myqr.run(content, picture=path, colorized=True, save_name=save_name)
        except:
            ver, ecl, qr_name = myqr.run(content, picture=path, colorized=False, save_name=save_name)
        with open(save_name, 'rb') as output:
            hook(output)
        os.remove(save_name)
        return fp


if __name__ == '__main__':
    ver, ecl, qr_name = myqr.run("http://hackupc.com/", picture="/Users/Security/Downloads/120575-200.png", contrast=1.,save_name='pen.png')

# ver, ecl, qr_name = myqr.run("http://goatse.ru/", picture="/Developer/PycharmProjects/WhereToGo/dick.jpg", colorized=False, save_name='dick_qr.jpg')