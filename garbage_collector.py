from get_image import AVAILABLE_FORMATS
import glob
import os

def delete_images():
    current_pwd = os.getcwd()
    globs = [os.path.join(current_pwd, '*.' + extention) for extention in AVAILABLE_FORMATS]
    for gl in globs:
        for path in glob.glob(gl):
            os.remove(path)

if __name__ == '__main__':
    delete_images()
