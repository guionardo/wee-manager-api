import os

import uvicorn

from src.app.__main__ import app

PORT = int(os.environ.get('PORT', '8000'))


def main():
    uvicorn.run(app, host='0.0.0.0', port=PORT)


if __name__ == '__main__':
    main()
