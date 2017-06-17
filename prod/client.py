import subprocess
import keyboard
import shlex
import requests
from clipboard import ClipBoard

def load_image(tag):
    print('loding tag:', tag)
    requests.get('http://localhost:5000')
    r = requests.get('http://localhost:5000/get_image/{}'.format(tag))
    print('tag:', tag)
    if r.status_code == 200 and r.text:
        path = r.text
        ClipBoard.paste(path, tag)
    print(repr(tag))


# load_image('funny')
while True:
    keyboard.wait('alt+x')
    p = subprocess.Popen(shlex.split('py -3 _client.py'),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         universal_newlines=True)

    print('requesting')
    tag = p.stdout.readlines()[0].strip()
    if tag:
        load_image(tag)
    else:
        print('no tag')

