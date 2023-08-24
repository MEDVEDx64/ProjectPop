import os

from sys import argv
from uuid import uuid4

SRCD = 'src'
HEVCD = 'hevc'
XD = 'dataset/x'
YD = 'dataset/y'

# Handle input videos as Play of Game's exported from OW.
# Intro and outro parts will be omitted.
POG_MODE = True

def space_destroyer(path):
    if ' ' in path:
        os.rename(path, path.replace(' ', '_'))

def make_it_hevc(path):
    path = path.replace(' ', '_')
    os.system('ffmpeg -i ' + os.path.join(SRCD, path) + ' -an -vf scale=960:-1 -crf 26 -c:v libx265 -y ' + os.path.join(HEVCD, path))

def go_thru_files():
    files = os.listdir(SRCD)
    for n in files:
        space_destroyer(os.path.join(SRCD, n))
        make_it_hevc(n)

def chop_chop(path):
    hev_path = os.path.join(HEVCD, path)
    if not os.path.exists(hev_path):
        print('Warning: hevc file missing: ' + path)
        return

    i = str(uuid4())
    if POG_MODE:
        os.system('ffmpeg -i ' + os.path.join(SRCD, path) + ' -ss 5.5 -t 11.4 -y ' + os.path.join(YD, i) + '_%09d.png')
        os.system('ffmpeg -i ' + hev_path + ' -ss 5.5 -t 11.4 -y ' + os.path.join(XD, i) + '_%09d.png')
    else:
        os.system('ffmpeg -i ' + os.path.join(SRCD, path) + ' -y ' + os.path.join(YD, i) + '_%09d.png')
        os.system('ffmpeg -i ' + hev_path + ' -y ' + os.path.join(XD, i) + '_%09d.png')

def cook_frames():
    files = os.listdir(SRCD)
    for n in files:
        chop_chop(n)

def main():
    if len(argv) < 2:
        print('subcommands are: hevc, frames')
        return

    if argv[1] == 'hevc':
        go_thru_files()
    elif argv[1] == 'frames':
        cook_frames()
    else:
        print('???')

if __name__ == '__main__':
    main()
