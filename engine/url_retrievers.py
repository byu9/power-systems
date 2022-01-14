#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
from urllib.request import urlretrieve
from abc import ABC, abstractmethod
from pathlib import Path
import logging

class AbstractUrlRetriever(ABC):
    @property
    @abstractmethod
    def download_url(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def filename(self):
        raise NotImplementedError

    @property
    def path_and_filename(self):
        return self._path_and_filename

    def download_into(self, folder):
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)

        path_and_filename = folder / self.filename
        self._path_and_filename = path_and_filename

        if path_and_filename.exists():
            logging.info('Skipped downloading {} from {}'.format(
                path_and_filename, self.download_url))
        else:
            logging.info('Downloading {} from {}'.format(
                path_and_filename, self.download_url))

            urlretrieve(self.download_url, path_and_filename)
