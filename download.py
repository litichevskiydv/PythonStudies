import os
import re
import pathlib
import argparse
from urllib.request import urlopen, Request


def get_filename(response):
    filename = re.match(r'.*filename=\"(.+)\".*', response.headers["content-disposition"]).group(1)

    filename_bytes = []
    for character in filename:
        character_bytes = character.encode('cp1252', 'ignore')
        if len(character_bytes) > 0:
            filename_bytes.append(character_bytes[0])
        else:
            filename_bytes.append(character.encode('utf-8')[1])

    return bytes(filename_bytes).decode('utf-8')


def main():
    parser = argparse.ArgumentParser(add_help=True, description='Downloads file from site')
    parser.add_argument('--download-path', type=pathlib.Path)
    args = parser.parse_args()

    request = Request(
        url='...',
        headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36',
            'accept': '*/*'
        }
    )
    with urlopen(request) as response:
        file_path = os.path.join(args.download_path if args.download_path is not None else '...', get_filename(response))
        file_content = response.read()
        with open(file_path, 'wb') as file:
            file.write(file_content)


if __name__ == '__main__':
    main()
