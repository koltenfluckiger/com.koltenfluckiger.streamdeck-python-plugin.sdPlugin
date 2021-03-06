import platform
import logging
import sys
from pathlib import PurePosixPath, PureWindowsPath
from enum import Enum


class OSTYPE(Enum):

    WINDOWS = 1
    UNIX = 2
    MACOS = 3


class OSManager(object):

    def __init__(self):
        self._setup()

    def _setup(self):
        try:
            os_type = platform.system().lower()
            if 'windows' in os_type:
                self.OSTYPE = OSTYPE.WINDOWS
                self.binary_path = PureWindowsPath("pythonw.exe")
            else:
                self.OSTYPE = OSTYPE.UNIX
                self.binary_path = PurePosixPath('/usr/bin/env python')
        except Exception as err:
            logging.critical('ERROR AT _setup: {}'.format(err))

    def _get_current_os(self):
        try:
            return self.OSTYPE
        except Exception as err:
            logging.critical(err)

    def _get_current_binary_path(self):
        try:
            return self.binary_path
        except Exception as err:
            logging.critical(err)

    def convert_path(self, path):
        try:
            if self.OSTYPE == OSTYPE.WINDOWS:
                return PureWindowsPath(path)
            else:
                return PurePosixPath(path)
        except Exception as err:
            logging.critical('ERROR AT convert_path: {}'.format(err))

    def generate_exec_path(self, path, args):
        try:
            path = self.convert_path(path)
            full_path = self.convert_path(
                '{} {}'.format(self.binary_path, path))
            return '{} {}'.format(full_path, args)
        except Exception as err:
            logging.critical('ERROR AT generate_exec_path: {}'.format(err))
