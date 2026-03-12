import logging
try:
    import platform
    if 'windows' in platform.system().lower():
        from plyer.platforms.win.notification import instance as WinInstance
    elif 'linux' in platform.system().lower():
        from plyer.platforms.linux.notification import instance as LinuxInstance
    elif 'mac' in platform.system().lower():
        from plyer.platforms.macosx.notification import instance as OSXInstance
except ImportError as err:
    logging.critical(f"Import error: {err}")

from operatingsystem import OSTYPE

class Notifier():

    def __init__(self, os_type):
        if os_type == OSTYPE.WINDOWS:
            self.instance = WinInstance()
        elif os_type == OSTYPE.UNIX:
            self.instance = LinuxInstance()
        elif os_type == OSTYPE.MACOS:
            self.instance = OSXInstance()

    def notify(self, title, message):
        try:
            self.instance.notify(title=title, message=message)
        except Exception as err:
            logging.critical(f"Notify Error: {err}")
