"""Creates small thumbnails and works on raw images"""
from core.singleton import Singleton
from werkzeug.utils import secure_filename
import os
from io import BytesIO
import uuid
from PIL import Image

ALLOWED_EXTENSION = set('text pdf png jpg jpeg gif'.split())


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


# works as a singleton.
class ImageFileManager(metaclass=Singleton):
    """Creates small thumbnails and works on raw images"""

    QUAL = 2  # size of generated image is (400 * QUAL, 300 * QUAL).

    # higher means better for large images but worst for smaller.

    def __init__(self, folder, thumb_folder):
        """
        :param folder: where to save big images
        :param thumb_folder where to save thumbnail
        """
        self.folder = folder  # path for
        path = os.path.dirname(os.path.abspath(__file__))
        self.upload_folder = os.path.join(path, folder)  # abs path for folder
        self.thumbnail_folder = os.path.join(path, thumb_folder)  # abs path for folder

    def delete_file(self, file):
        os.remove(os.path.join(self.thumbnail_folder, file))
        os.remove(os.path.join(self.upload_folder, file))

    def get_thumbnail(self, path):
        """
        Generates thumbnail
        :param path: path to file
        :return: ByteIO object containing image
        """
        file_path = os.path.join(self.upload_folder, secure_filename(path))
        image = Image.open(file_path)  # open image
        self._make_small(image)  # make it small
        # generate it in the middle
        img_w, img_h = image.size
        background = Image.new('RGBA', (400 * self.QUAL, 300 * self.QUAL), (255, 255, 255, 255))
        bg_w, bg_h = background.size
        offset = (bg_w - img_w) // 2, (bg_h - img_h) // 2
        background.paste(image, offset)
        # save it to file
        fake_file = BytesIO()
        background.save(fake_file, 'PNG')
        fake_file.seek(0)  # make file 'readable'
        return fake_file

    def _make_small(self, img):
        img.thumbnail((400 * self.QUAL, 300 * self.QUAL))

    def new(self, file):
        """Saves image in upload_path.

        :param file: file from request.files.getlist
        :return:
            original_filename: file name after securing it
            random_filename: name of saved file. Random and unique (i hope lol)
        """
        if file and allowed_file(file.filename):
            original_filename = secure_filename(file.filename)  # delete weird thinks
            random_filename = str(uuid.uuid4()) + '.' + original_filename.split('.')[1]  # generate rand filename
            img = Image.open(file)
            self._make_small(img)
            file.seek(0)
            img.save(file, 'PNG')
            file.seek(0)
            file.save(os.path.join(self.upload_folder, random_filename))  # save it to uploads folder
            # now make another copy with white background
            img_w, img_h = img.size
            background = Image.new('RGBA', (img_w, img_h), (255, 255, 255, 255))
            bg_w, bg_h = background.size
            offset = (bg_w - img_w) // 2, (bg_h - img_h) // 2
            background.paste(img, offset)
            # save it to file
            background.save(os.path.join(self.thumbnail_folder, random_filename), 'PNG')
            file.seek(0)

        else:
            raise AttributeError('File is no allowed or do not exist.')

        return original_filename, random_filename
