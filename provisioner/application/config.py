class Config(object):
    __CONFIG = {}
    __TYPES = {
        'machine': ('desktop', 'server', 'apache', 'lemp', 'mqtt'),
        'program': ('php', 'nodejs'),
        'os': ('debian', 'ubuntu', 'raspberry pi')
    }

    def get(self, key: str, default=None):
        return self.__CONFIG.get(key, default)

    def set(self, key: str, value):
        self.__CONFIG[key] = value

    def is_valid_type(self, type_key: str, type_value) -> bool:
        return type_value in self.__TYPES[type_key]
