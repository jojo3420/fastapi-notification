from typing import Optional
from dataclasses import asdict

from fastapi import FastAPI
import uvicorn
from app.common.config import conf
from devtools import debug


def create_app():
    """앱 생성"""

    app = FastAPI()
    config = conf()
    # 데이터베이스 초기화

    # 레디스 초기화

    # 미들웨어 정의

    # 라우터 정의

    return app


app = create_app()


@app.get('/')
def health_check():
    return {'health_check': 'ok'}


if __name__ == '__main__':
    uvicorn.run('app.main:app', port=8000, reload=conf().PROJ_RELOAD)
