#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
import logging


def is_interactive():
    import sys
    return hasattr(sys, 'ps1')



if is_interactive():
    class Multiprocessing_Pool:
        def __init__(self):
            from pathos.multiprocessing import ProcessingPool
            logging.debug('Using pathos multiprocessing')
            self._backend = ProcessingPool()

        def __enter__(self):
            return self._backend.__enter__()

        def __exit__(self, *args):
            self._backend.__exit__(*args)

        def map(self, f, seq):
            return self._backend.map(f, seq)

else: # not running interactively
    class Multiprocessing_Pool:
        def __init__(self):
            from multiprocessing.pool import Pool
            logging.debug('Using python built-in multiprocessing')
            self._backend = Pool()

        def __enter__(self):
            return self._backend.__enter__(*args)

        def __exit__(self, *args):
            self._backend.__exit__(*args)

        def map(self, f, seq):
            return self._backend.map(f, seq)





class Remote_File:
    def __init__(self, url, download_name):
        self.url = url
        self.download_name = download_name

    def download_into(self, folder):
        from pathlib import Path
        from urllib.request import urlretrieve

        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        self.filename = folder / self.download_name

        if self.filename.exists():
            logging.debug('Skipped downloading "{}" from "{}"'.format(
                self.filename, self.url))
        else:
            logging.debug('Downloading "{}" from "{}"'.format(
                self.filename, self.url))

            urlretrieve(self.url, self.filename)




class Compressed_File:
    def __init__(self, filename):
        self.filename = filename

    def extract_into(self, folder):
        from pathlib import Path
        from shutil import unpack_archive

        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)

        logging.debug('Extracing "{}" into "{}"'.format(self.filename, folder))
        unpack_archive(self.filename, folder)
