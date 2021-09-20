import pickle


class DataAccessObject:
    def __init__(self, datasource, instance):
        self.__datasource = datasource
        self.__instance = instance
        self.__cache = {}
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, 'wb'))

    def __load(self):
        self.__cache = pickle.load(open(self.__datasource, 'rb'))

    def add(self, key, obj, force_insert=False):
        if obj is not None and (isinstance(obj, self.__instance) or force_insert):
            self.__cache[key] = obj
            self.__dump()

    def get(self, key):
        try:
            return self.__cache[key]
        except KeyError:
            pass

    def remove(self, key):
        try:
            self.__cache.pop(key)
            self.__dump()
        except KeyError:
            print('Error at remove')

    def get_all(self):
        return list(self.__cache.values())
