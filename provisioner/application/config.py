class Config(object):
    __CONFIG = {}
    __TYPES = {
        'machine': ('desktop', 'server', 'lemp', 'mqtt'),
        'program': ('mariadb', 'nodejs', 'php', 'redis'),
        'os': ('ubuntu', 'raspberry pi')
    }

    def get(self, key: str, default=None):
        return self.__CONFIG.get(key, default)

    def set(self, key: str, value):
        self.__CONFIG[key] = value

    def validate_type(self, key: str, type_: str) -> bool:
        return type_ in self.__TYPES[key]
