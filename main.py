import logging
import pathlib
import platform

import waitress
from tap import Tap

from hackathon import create_app

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)


class ServerType(Tap):
    production: bool

    def configure(self) -> None:
        self.add_argument('--production', '-p', action='store_true', default=False,
                          help='Whether to run the server in production mode')


if __name__ == '__main__':

    pathlib.Path('ffmpeg').mkdir(exist_ok=True)
    platform_name = platform.system()
    if platform_name == 'Windows':
        executable = pathlib.Path('ffmpeg/ffmpeg.exe')
        download_url = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'
    elif platform_name == 'Darwin':
        executable = pathlib.Path('ffmpeg/ffmpeg-darwin')
        download_url = 'https://evermeet.cx/ffmpeg/ffmpeg-6.0.zip'

    if not executable.exists():
        print("FFmpeg not found, downloading...")
        import io
        import zipfile

        import requests

        r = requests.get(download_url)
        temp = io.BytesIO(r.content)
        with zipfile.ZipFile(temp) as z:
            if platform_name == 'Windows':
                z.extract('ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe', 'ffmpeg')
                pathlib.Path('ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe').rename('ffmpeg/ffmpeg.exe')
                pathlib.Path('ffmpeg/ffmpeg-master-latest-win64-gpl/bin').rmdir()
                pathlib.Path('ffmpeg/ffmpeg-master-latest-win64-gpl').rmdir()
            elif platform_name == 'Darwin':
                z.extract('ffmpeg', 'ffmpeg')

    args = ServerType().parse_args()
    if args.production:
        waitress.serve(create_app(), host='127.0.0.1', port=5000)
    else:
        create_app().run(host='127.0.0.1', port=5000, debug=True)
