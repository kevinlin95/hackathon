import logging

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
    args = ServerType().parse_args()
    if args.production:
        waitress.serve(create_app(), host='127.0.0.1', port=5000)
    else:
        create_app().run(host='127.0.0.1', port=5000, debug=True)
