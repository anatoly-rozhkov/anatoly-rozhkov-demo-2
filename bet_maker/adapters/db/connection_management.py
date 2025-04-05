from typing import Dict, Type


class DBConnectionManagement(type):
    _instances: Dict[Type, Dict[str, object]] = {}

    def __call__(cls, key: str, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = {}

        if key not in cls._instances[cls]:
            # Create an instance if it doesn't exist for the provided key
            cls._instances[cls][key] = super(DBConnectionManagement, cls).__call__(*args, **kwargs)

        return cls._instances[cls][key]
