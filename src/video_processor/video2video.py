#!/usr/bin/env python3

from sys import argv

from v2v import model, ffmpeg
from v2v.picture import create_frame, unpack_frame
from v2v.exception import V2VUserException

def print_help():
    print('usage: ' + argv[0] + ' <model_descfile> <infile> <outfile>')

def main():
    if len(argv) < 4:
        print_help()
        return
    
    descfile, infile, outfile = tuple(argv[1:4])

    try:
        m = model.PictureProcessorModel(descfile)
        with ffmpeg.FfmpegReadingProcess(m.description, infile) as reader:
            with ffmpeg.FfmpegWritingProcess(m.description, outfile, ffmpeg.fetch_vfinfo(infile)) as writer:
                def callback(bytes_: bytes):
                    writer.push(unpack_frame(m.model.predict(create_frame(bytes_))))

                reader.run(callback)

    except V2VUserException as e:
        print('Error: ' + str(e))

if __name__ == '__main__':
    main()
