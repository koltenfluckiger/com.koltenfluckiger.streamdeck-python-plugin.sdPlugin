try:
    from operatingsystem import OSTYPE
    import platform
    import logging
    import traceback
    if 'windows' in platform.system().lower():
        from pywintoaster.toaster import Toaster
    elif 'linux' in platform.system().lower():
        from plyer.platforms.linux.notification import instance as LinuxInstance
    elif 'mac' in platform.system().lower():
        from plyer.platforms.macosx.notification import instance as OSXInstance
except ImportError as err:
    logging.critical("Import error: {}".format(err))
    logging.critical(f"Traceback: {traceback.format_exc()}")

class Notifier():

    def __init__(self, OS):
        if OS == OS.WINDOWS:
            self.instance = Toaster(group="StreamDeck Python Plugin")
        elif OS == OS.UNIX:
            self.instance = LinuxInstance()
        elif OS == OS.MACOS:
            self.instance = OSXInstance()

    def notify(self, title, message):
        try:
            self.instance.notify(title=title, message=message)
        except Exception as err:
            logging.critical("Notify Error: {}".format(err))
            logging.critical(f"Traceback: {traceback.format_exc()}")
