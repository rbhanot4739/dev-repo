import os

from PIL import Image
from hashlib import md5
from . import app


def process_image(filename, username):
    fname, ext = filename.split('.')
    new_name = md5(
        username.encode() + fname.encode()).hexdigest() + '.' + ext
    new_path = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
    old_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    pic = Image.open(old_path)
    pic.thumbnail((125, 125))
    pic.save(new_path)
    os.remove(old_path)
    return new_name
