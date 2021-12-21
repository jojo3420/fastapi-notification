from dataclasses import dataclass, field
from os import path, environ
from devtools import debug
from functools import lru_cache
from pydantic import BaseSettings, SecretStr
import json

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


env = {}
with open(base_dir + "/.env") as f:
    for line in f.readlines():
        k, v = line.strip().split("=")
        env[k] = v


@dataclass
class Config:
    """
    기본 환경 설정 데이터 클래스
    데이터클래스에 대해서 자세히..
    https://www.daleseo.com/python-dataclasses/
    """

    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = True
    DB_URL: str = f'mysql+pymysql://{env.get("DB_USERNAME")}:{env.get("DB_PASSWORD")}@{env.get("DB_HOST")}:{env.get("DB_PORT")}/{env.get("DB_SCHEMA")}'


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
    return config.get(environ.get("API_ENV", "local"))


# class Settings(BaseSettings):
#     """환경변수"""
#
#     DB_USERNAME: str
#     DB_PASSWORD: SecretStr
#     DB_HOST: str
#     DB_PORT: str
#     DB_SCHEMA: str
#
#     JWT_SECRET_KEY: SecretStr
#     TESTING: bool
#
#     class Config:
#         env_file = ".env"
#         env_file_encoding = "UTF-8"


# settings 은 앱에서 자주사용하므로 캐싱을 한다.
# Least Recently-Used cache decorator
# @lru_cache
# def get_settings():
#     return Settings()


# settings = get_settings()
