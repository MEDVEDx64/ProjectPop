import subprocess
import shutil
import re

from .exception import V2VConfigurationError
from .model import ModelDescription

class VideoFileInfo(object):
    REGEX = r'^[0-9]+\/[0-9]+$'

    def __init__(self, framerate_frac='60/1'):
        if not re.match(VideoFileInfo.REGEX, framerate_frac):
            raise ValueError('framerate fraction must be in xx/yy format')
        
        self.framerate_frac = framerate_frac


class FfmpegProcess(object):
    def __init__(self, model_desc: ModelDescription, file_path: str):
        self.ffmpeg_path = shutil.which('ffmpeg')
        if not self.ffmpeg_path:
            raise V2VConfigurationError('ffmpeg not found')
        
        self._stdin = None
        self._stdout = None
        self._model_desc = model_desc
        self._file_path = file_path

    def _build_args(self) -> list[str]:
        raise NotImplementedError()


class FfmpegWritingProcess(FfmpegProcess):
    def __init__(self, model_desc: ModelDescription, file_path: str, vfinfo: VideoFileInfo):
        super().__init__(model_desc, file_path)
        self._vfinfo = vfinfo
        self._stdin = subprocess.PIPE

        self._process = subprocess.Popen(
            self._build_args(),
            stdin=self._stdin,
            stdout=self._stdout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._process.stdin.close()
        self._process.wait()

    def _build_args(self) -> list[str]:
        w, h = self._model_desc.output_dimensions
        return [self.ffmpeg_path,
                '-f', 'rawvideo',
                '-pix_fmt', 'rgb24',
                '-s:v', str(w) + 'x' + str(h),
                '-r', self._vfinfo.framerate_frac,
                '-i', '-',
                '-pix_fmt', 'yuv420p10le',
                '-c:v', 'libsvtav1',
                '-preset', '6',
                '-crf', '28',
                '-y',
                self._file_path]

    def push(self, data: bytes):
        self._process.stdin.write(data)


class FfmpegReadingProcess(FfmpegProcess):
    def __init__(self, model_desc: ModelDescription, file_path: str):
        super().__init__(model_desc, file_path)
        self._stdout = subprocess.PIPE

        self._process = subprocess.Popen(
            self._build_args(),
            stdin=self._stdin,
            stdout=self._stdout)
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._process.terminate()

    def _build_args(self) -> list[str]:
        w, h = self._model_desc.input_dimensions
        return [self.ffmpeg_path, '-i', self._file_path,
                '-an', '-pix_fmt', 'rgb24',
                '-vf', 'scale=' + str(w) + ':' + str(h),
                '-f', 'rawvideo',
                '-hide_banner',
                '-loglevel', 'error',
                'pipe:1'
                ]
    
    def run(self, read_callback) -> None:
        w, h = self._model_desc.input_dimensions
        read_size = w * h * 3
        while True:
            bytes_ = self._process.stdout.read(read_size)
            if len(bytes_) < read_size:
                break

            read_callback(bytes_)


class FfmpegStillPictureProcess(FfmpegProcess):
    def __init__(self, model_desc: ModelDescription, file_path: str):
        super().__init__(model_desc, file_path)


def fetch_vfinfo(file_path: str) -> VideoFileInfo:
    ffprobe_path = shutil.which('ffprobe')
    if not ffprobe_path:
        raise V2VConfigurationError('ffprobe not found')
    
    process = subprocess.Popen([ffprobe_path,
                                '-v', '0', '-of', 'csv=p=0',
                                '-select_streams', 'v:0',
                                '-show_entries', 'stream=r_frame_rate',
                                file_path],
                                stdout=subprocess.PIPE,
                                text=True)
    
    value = process.stdout.readline()
    process.terminate()
    return VideoFileInfo(value)
