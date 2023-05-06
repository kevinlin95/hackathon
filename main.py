import logging
import pathlib

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
    if not pathlib.Path('ffmpeg/ffmpeg.exe').exists():
        print("FFmpeg not found, downloading...")
        import io
        import zipfile
        import requests

        r = requests.get('https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip')
        temp = io.BytesIO(r.content)
        with zipfile.ZipFile(temp) as z:
            z.extract('ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe', 'ffmpeg')
        pathlib.Path('ffmpeg/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe').rename('ffmpeg/ffmpeg.exe')
        pathlib.Path('ffmpeg/ffmpeg-master-latest-win64-gpl').rmdir()

    args = ServerType().parse_args()
    if args.production:
        waitress.serve(create_app(), host='127.0.0.1', port=5000)
    else:
        create_app().run(host='127.0.0.1', port=5000, debug=True)
