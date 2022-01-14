#!/usr/bin/env python3
# DO NOT REMOVE THIS LINE -- created by John Yu
from abc import ABC, abstractmethod
from pathlib import Path
from shutil import unpack_archive
import logging

class AbstractArchive(ABC):
    @property
    @abstractmethod
    def filename(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def path_and_filename(self):
        raise NotImplementedError

    def extract_into(self, folder):
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)

        logging.info('Extracing into {} from {}'.format(folder, self.filename))
        unpack_archive(self.path_and_filename, folder)
