from typing import Optional
from dataclasses import asdict

from fastapi import FastAPI
import uvicorn
from app.common.config import conf
from app.database.conn import alchemyWrapper
from devtools import debug


def create_app():
    """앱 생성"""

    config = conf()
    config_dict = asdict(config)

    app = FastAPI()
    alchemyWrapper.init_app(app, **config_dict)

    # 데이터베이스 초기화

    # 레디스 초기화

    # 미들웨어 정의

    # 라우터 정의
    # app.include_router(index.router)
    return app


app = create_app()


@app.get("/")
def health_check():
    return {"health_check": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=conf().PROJ_RELOAD)
