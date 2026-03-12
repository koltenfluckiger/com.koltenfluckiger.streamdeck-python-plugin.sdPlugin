import platform
import logging
from pathlib import PurePosixPath, PureWindowsPath, Path
from enum import Enum

logger = logging.getLogger()

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
            elif 'darwin' in os_type:
                self.OSTYPE = OSTYPE.MACOS
                self.binary_path = PurePosixPath('/usr/bin/env python')
            else:
                self.OSTYPE = OSTYPE.UNIX
                self.binary_path = PurePosixPath('/usr/bin/env python')
        except Exception as err:
            logger.critical(f'ERROR AT _setup: {err}')

    def _get_current_os(self):
        try:
            return self.OSTYPE
        except Exception as err:
            logger.critical(err)

    def _get_current_binary_path(self):
        try:
            return self.binary_path
        except Exception as err:
            logger.critical(err)

    def convert_path(self, path):
        try:
            return Path(rf"{path}").resolve()
        except Exception as err:
            logger.critical(f'ERROR AT convert_path: {err}')

    def generate_exec_path(self, path, args):
        try:
            path = self.convert_path(path)
            logger.info(f"Path: {path}")
            full_command = f"{self.binary_path} {path} {args}"
            logger.info(f"Full command: {full_command}")
            return full_command
        except Exception as err:
            logger.critical(f'ERROR AT generate_exec_path: {err}')
