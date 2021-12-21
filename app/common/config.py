from dataclasses import dataclass, asdict
from os import path, environ
from devtools import debug

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class Config:
    """
    기본 환경 설정 데이터 클래스
    """
    BASE_DIR: str = base_dir

    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True


@dataclass
class LocalConfig(Config):
    """
    로컬 환경 설정
    """
    PROJ_RELOAD: bool = True


@dataclass
class ProdConfig(Config):
    """
    운영 환경 설정
    """
    PROJ_RELOAD: bool = False


def conf():
    """
    환경 설정 불러 오기
    :return: Config
    """
    config = dict(prod=ProdConfig(), local=LocalConfig())
    return config.get(environ.get('API_ENV', 'local'))
