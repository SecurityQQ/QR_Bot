from qrcode.MyQR import myqr
from get_image import get_smart_image, download_image, is_url
from random import randint
import os

def smart_qr_code(content, source, colorized=True, suffix=".png", save_name=None, hook=lambda x: x):
    if is_url(source):
        raw_image = download_image(source)
    else:
        raw_image = get_smart_image(source)
    if raw_image is None:
        hook(None)
        return

    random_suffix = str(randint(1, 100000))

    current_pwd = os.getcwd()
    tmp_file_name = "tmp" + random_suffix + suffix
    temp_file_path = os.path.join(current_pwd, tmp_file_name)

    if save_name is None:
        save_name = "qr_code_" + tmp_file_name

    with open(temp_file_path, 'wb+') as temp_file:
        temp_file.write(raw_image)

    try:
        ver, ecl, qr_name = myqr.run(content, picture=temp_file_path, colorized=colorized, save_name=save_name)
    except:
        ver, ecl, qr_name = myqr.run(content, picture=temp_file_path, colorized=False, save_name=save_name)

    with open(save_name, 'rb') as output:
        hook(output)

    os.remove(save_name)
    os.remove(temp_file_path)



if __name__ == '__main__':
    smart_qr_code('I want to hide this secret message', 'peka')