import subprocess
import keyboard
import requests
import sys, os
from PyQt5.QtCore import QThread


try:
    from clipboard import ClipBoard
    from core import path
except ImportError:
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    from clipboard import ClipBoard
    from core import path




def load_image(tag):
    print('Loading tag:', tag)
    try:
        r = requests.get('{}get_image/{}'.format(path.host_name, tag), data='siemka')
    except:
        # TODO: change this exeption
        print('Server is offine')
    else:
        print('Loading complete')
        if r.status_code == 200 and r.text:
            print('ok')
            reply = r.text
            ClipBoard.paste(reply, tag)


# load_image('funny')

def run():
    client_path = '{} {}'.format(path.pythonw, path.get('client/_client.py'))
    p = subprocess.Popen(client_path,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         universal_newlines=True)
    # FIXME: stop using popen REALLLY I HAVE NO IDEA HOW TO OVERCOME THIS
    # Two times i thied to to this with threading: Pythonic and QThread but when called this way
    # it unclickable or isnt at the top
    for tags in p.stdout.readline():
        print('Waithing for input')
        keyboard.wait('alt+x')
        tag = tags
        print(2)
        if tag and tag[0].strip():
            tag = tag[0].strip()
            load_image(tag)
        else:
            print('Tag not found')


if __name__ == '__main__':
    run()
