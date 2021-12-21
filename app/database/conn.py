import logging

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from devtools import debug


def _database_exist(engine, schema_name):
    query = (
        f"SELECT schema_name FROM information_schema WHERE schema_name = {schema_name}"
    )
    with engine.connect() as conn:
        result_proxy = conn.execute(query)
        result = result_proxy.scalar()
        debug(result)
        return bool(result)


class SQLAlchemyWrapper:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        """
        DB 초기화 함수
        :params app: FastAPI 인스턴스
        :params kwargs:
        """

        db_url = kwargs.get("DB_URL")
        pool_recycle = kwargs.get("DB_POOL_RECYCLE", 900)
        echo = kwargs.get("DB_ECHO", True)

        self._engine = create_engine(
            db_url,
            echo=echo,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
        )
        self._session = sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine
        )

        @app.on_event("startup")
        def startup():
            self._engine.connect()
            logging.info("DB Connected.")

        @app.on_event("shutdown")
        def shutdown():
            self._session.cllose_all()
            self._engine.dispose()
            logging.info("DB Disconnected.")

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine

    def get_db(self):
        """요청마다 DB 세션 유지함수"""
        if self._session is None:
            raise Exception("Must be called init_app() func!")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            if db_session:
                db_session.close()


alchemyWrapper = SQLAlchemyWrapper()
Base = declarative_base()
# _database_exist(alchemyWrapper.engine, '')
