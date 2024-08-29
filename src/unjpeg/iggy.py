import os

from sys import argv
from uuid import uuid4

SRCD = 'src'
XD = 'dataset/x'
YD = 'dataset/y'

def space_destroyer(path):
    if ' ' in path:
        os.rename(path, path.replace(' ', '_'))

def go_thru_files():
    files = os.listdir(SRCD)
    for n in files:
        space_destroyer(os.path.join(SRCD, n))

def chop_chop(path):
    i = str(uuid4())
    src_path = os.path.join(SRCD, path)

    os.system('ffmpeg -i ' + src_path + ' -vf scale=1920:1080 -y ' + os.path.join(YD, i) + '_%09d.png')
    os.system('ffmpeg -i ' + src_path + ' -vf scale=1920:1080 -y -q 3 ' + os.path.join(XD, i) + '_%09d.jpg')

def cook_frames():
    files = os.listdir(SRCD)
    for n in files:
        chop_chop(n)

def main():
    if len(argv) < 2:
        print('subcommands are: frames')
        return

    elif argv[1] == 'frames':
        cook_frames()
    else:
        print('???')

if __name__ == '__main__':
    main()
