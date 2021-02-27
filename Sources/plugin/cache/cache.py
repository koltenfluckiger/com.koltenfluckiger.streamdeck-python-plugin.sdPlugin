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
            print(err)

    def _init_cache(self, uuid):
        try:
            self.cache[uuid] = {}
        except Exception as err:
            print(err)
