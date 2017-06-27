import subprocess
import keyboard
import requests
import sys, os

from clipboard import ClipBoard
from shubi_files.core import path


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
    while True:
        client_path = '{} {}'.format(path.pythonw, path.get('client/_client.py'))
        keyboard.wait('alt+x')
        p = subprocess.Popen(client_path,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             universal_newlines=True)

        tag = p.stdout.readlines()
        if tag and tag[0].strip():
            tag = tag[0].strip()
            load_image(tag)
        else:
            print('Tag not found')


if __name__ == '__main__':
    run()
