from dataclasses import dataclass, asdict
from os import path, environ

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    """
    기본 환경 설정 데이터 클래스
    """
    BASE_DIR = base_dir
    DB_POOL_RECYCLE = 900
    DB_ECHO = True


@dataclass
class LocalConfig(Config):
    PROJ_RELOAD = True


class ProductConfig(Config):
    PROJ_RELOAD = False


def conf():
    """ 환경설정 불러오기 """
    config = dict(prod=ProductConfig(), local=LocalConfig())
    return config.get(environ.get('API_ENV', 'local'))
