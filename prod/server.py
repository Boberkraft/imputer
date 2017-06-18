from flask import Flask, request, render_template, send_file, redirect, url_for, send_from_directory
from flask_cors import CORS, cross_origin
from flask_babel import Babel
from imagemanager import image_file_M
from PIL import Image, ImageOps
from io import BytesIO
import threading
import os
import uuid
from flask_babel import gettext as _
import database as Database
from user import User

app = Flask(__name__, static_folder='files', static_url_path='')
CORS(app)
babel = Babel(app)
ALLOWED_MODE = ('selected', 'database')
ALLOWED_ACTION = ('add', 'select', 'delete', 'unselect')

LANGUAGES = {
    'en': 'English',
    'pl': 'Polish'
}
# BABEL
print(_('elo'))
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())

class Config:
    navigation_tabs = [('/', _('Menu')),
                       ('/add/', _('Add')),
                       ('/upload/', _('Search')),
                       ('/update/', _('About'))]

    images_path = '/uploads/'


old_render_template = render_template


def render_template(*args, **kwargs):
    return old_render_template(*args, **kwargs, config=Config)


@app.route('/upload_files/', methods=['GET', 'POST'])
def upload_files():
    images = []
    if request.method == 'POST':
        files = request.files.getlist('files[]')  # get uploaded files
        for file in files:
            name, random = image_file_M.new(file)  # add files to disc and return filenames
            images.append(dict(name=random, original_name=name, file=random))  # just like in database
    User.upload(images)  # upload them to database
    images = User.get_uploaded()  # return uploaded images
    return render_template('cards.html', images=images)


@app.route('/change_state/', methods=['GET', 'POST'])
def change():
    # msg = { 'mode': 'xx',
    #         'status': 'xx',
    #         xx}
    msg = request.json
    print('New Change state:', msg)
    if msg:
        mode, action = msg['mode'], msg['action']
        if mode not in ALLOWED_MODE or action not in ALLOWED_ACTION:
            raise ValueError('Not allowed mode or action!')
        if mode == 'selected':
            if action == 'select':
                User.select(msg['id'])
            elif action == 'unselect':
                User.unselect(msg['id'])
            elif action == 'add':
                User.add_uploaded(msg['id'], msg['tags'])
            elif action == 'delete':
                id = msg.get('id', None)
                User.delete(id)

        elif mode == 'database':
            if action == 'add':
                User.add_selected()
            if action == 'delete':
                User.delete_selected()
        else:
            print('Undefinied mode!')
            return str('something went wrong.')
    return redirect(url_for('get_single_card', id=msg['id']))


@app.route('/uploads/<path:name>')
def get_files(name):
    """Returns thumbnail with this random name."""
    return send_from_directory('thumbs', name)
    # return send_file(image_file_M.get_thumbnail(name), mimetype='image/png')


@app.route('/add/')
def dodaj():
    """Page for adding more images"""
    # get loaded but not saved images
    images = User.get_uploaded()

    return render_template('add.html', images=images)


@app.route('/selected/')
def selected_page():
    """Page for working with selected images"""
    # get selected images
    images = User.get_selected()

    return render_template('selected.html', images=images)


@app.route('/upload/')
def upload_page():
    return render_template('upload.html')


@app.route('/update/')
def contact_page():
    news = news_page()
    return render_template('update.html', news=news)


@app.route('/image_card/<id>')
def get_single_card(id):
    id = id.strip()
    if id:
        image = User.get_by_id(id)
        if image:
            return render_template('card.html', image=image, save='hide', edit='')
    return 'Image with id = {} not found'.format(id)


@app.route('/news/')
def news_page():
    news = [
        {'date': 'czas',
         'content': 'Chyba teraz wszystko działa',
         'author': 'Andrzej Bisewski',
         'image': 'https://avatars3.githubusercontent.com/u/16669574',
         'github': '@Boberkraft'},
        {'date': 'czas',
         'content': 'Hello my first post',
         'author': 'Andrzej Bisewski',
         'image': 'https://avatars3.githubusercontent.com/u/16669574',
         'github': '@Boberkraft'}
    ]
    return news


@app.route('/get_image/<tag>')
def get_image_page(tag):
    print('GOT TAG', tag.strip())
    image = User.get_by_tag(tag)
    if image:
        return image
    return ''


@app.route('/')
def main():
    images = User.get_images()
    return render_template('index.html', images=images)

if __name__ == "__main__":
    # maybe move this to another file?
    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()

# TODO: searching by tag
# TODO: online server to upload/download pictures
# TODO: message to online server
# DONE: cache small pictures
# TODO: refactor User class, DO .ALL()
# TODO: refactor Database class
# TODO: redo Client just to make it work
# TODO: refactor server
# TODO: detect image duplicates
# TODO: do way do undo delete baceuse missclick
# TODO: block uploading without tags
# TODO: prograss bar
# TODO: when removing cards empty space is still there
