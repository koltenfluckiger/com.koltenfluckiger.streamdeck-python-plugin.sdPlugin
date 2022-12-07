import logging

class CacheManager(object):

    def __init__(self):
        self.cache = {}

    def _get_cache(self, uuid):
        try:
            if uuid in self.cache:
                return self.cache[uuid]
            else:
                return None
        except Exception as err:
            logging.critical(err)

    def _init_cache(self, uuid):
        try:
            self.cache[uuid] = {}
        except Exception as err:
            logging.critical(err)

    def _add_to_cache(self, uuid, key, value):
        try:
            self.cache[uuid][key] = value
        except Exception as err:
            logging.critical(err)

    def _remove_from_cache(self, uuid, key):
        try:
            del self.cache[uuid][key]
        except Exception as err:
            logging.critical(err)
