try:
    from operatingsystem import OSTYPE
    import platform
    import logging
    if 'windows' in platform.system().lower():
        from plyer.platforms.win.notification import instance as WinInstance
    elif 'linux' in platform.system().lower():
        from plyer.platforms.linux.notification import instance as LinuxInstance
    elif 'mac' in platform.system().lower():
        from plyer.platforms.macosx.notification import instance as OSXInstance
except ImportError as err:
    logging.critical("Import error: {}".format(err))


class Notifier():

    def __init__(self, OS):
        if OS == OS.WINDOWS:
            self.instance = WinInstance()
        elif OS == OS.LINUX:
            self.instance = LinuxInstance()
        elif OS == OS.MACOS:
            self.instance = OSXInstance()

    def notify(self, title, message):
        try:
            self.instance.notify(title=title, message=message)
        except Exception as err:
            logging.critical("Notify Error: {}".format(err))
