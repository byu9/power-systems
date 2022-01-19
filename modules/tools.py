#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
import logging

from pathlib import Path
from urllib.request import urlretrieve
from shutil import unpack_archive



class Remote_File:
    def __init__(self, url, download_name):
        self.url = url
        self.download_name = download_name

    def download_into(self, folder):
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        self.filename = folder / self.download_name

        if self.filename.exists():
            logging.info('Skipped downloading "{}" from "{}"'.format(
                self.filename, self.url))
        else:
            logging.info('Downloading "{}" from "{}"'.format(
                self.filename, self.url))

            urlretrieve(self.url, self.filename)




class Compressed_File:
    def __init__(self, filename):
        self.filename = filename

    def extract_into(self, folder):
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)

        logging.info('Extracing "{}" into "{}"'.format(self.filename, folder))
        unpack_archive(self.filename, folder)
