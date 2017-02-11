import os
import sys
import shutil
import eyed3
from PIL import Image


TMP_FOLDER = 'tmp'


class TemporaryFolder():
    def __init__(self, folder):
        self.folder = folder

    def __enter__(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)
        return os.path.abspath(self.folder)

    def __exit__(self, type, value, traceback):
        shutil.rmtree(self.folder)


def _tpath(fname):
    return os.path.join(TMP_FOLDER, fname)


def resize(root, f, width, height):
    fname = os.path.join(root, f)
    audiofile = eyed3.load(fname)

    if not audiofile:
        return

    print(fname)

    audio_img = []
    for img_info in audiofile.tag.images:
        imgname = '%s.%d' % (_tpath(f), img_info.picture_type)
        with open(imgname, 'w') as tf:
            tf.write(img_info.image_data)
        audio_img.append(
            (imgname, img_info.picture_type, img_info.description))

    for imgname, type_id, description in audio_img:
        im = Image.open(imgname)
        im2 = im.resize((width, height), Image.BILINEAR)
        im2.save(imgname, 'JPEG')

        imagedata = open(imgname, "rb").read()
        audiofile.tag.images.set(type_id,
                                 imagedata,
                                 'image/jpeg',
                                 description)
    audiofile.tag.save()


def main():
    if len(sys.argv) != 4:
        print('Invalid usage. Example: python %s folder_path width height'
              % sys.argv[0])
        exit()

    folder_path = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])

    with TemporaryFolder(TMP_FOLDER) as t_dirpath:
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                try:
                    resize(root, f, width, height)
                except NotImplementedError as e:
                    print("""
                          ----------------------------------
                          | {}
                          | {}
                          ----------------------------------
                          """.format(f, e))


if __name__ == '__main__':
    main()
