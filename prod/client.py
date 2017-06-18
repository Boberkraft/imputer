import subprocess
import keyboard
import shlex
import requests
from clipboard import ClipBoard


def load_image(tag):
    print('Loading tag:', tag)
    r = requests.get('http://localhost:5000/get_image/{}'.format(tag),data='siemka' )
    print('Loading complete')
    if r.status_code == 200 and r.text:
        path = r.text
        ClipBoard.paste(path, tag)


# load_image('funny')
while True:
    keyboard.wait('alt+x')
    p = subprocess.Popen(shlex.split('py -3 _client.py'),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         universal_newlines=True)

    print('requesting')
    tag = p.stdout.readlines()
    if tag and tag[0].strip():
        tag = tag[0].strip()
        load_image(tag)
    else:
        print('no tag')
