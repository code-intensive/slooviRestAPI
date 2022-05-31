import datetime
import yaml


DEFAULT_TOKEN_EXPIRY_TIME = 15


def getTokenExpirationTime(config_path:str="config.yml", minutes: int = None):
    if minutes is not None:
        if isinstance(minutes, int):
            return datetime.timedelta(minutes=minutes)
        raise TypeError(F'Expected argument of type int not { type(minutes) }')
    try:
        with open(config_path, "r") as ymlfile:
            cfgfile = yaml.load(ymlfile)
            expiration_time = cfgfile['TOKEN_EXPIRY_TIME']
    except Exception:
        expiration_time = DEFAULT_TOKEN_EXPIRY_TIME
    finally:
        return datetime.timedelta(minutes=expiration_time)
