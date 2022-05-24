from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app import tags_metadata
from app.routers import users, categories, products, promotions, tasks, staffs, orders, combo, banners, stores, \
    versions, search, location, notifications
from app.logger import AppLog
from starlette.requests import Request
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI(openapi_tags=tags_metadata.tags_metadata)


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        AppLog(request.url.path).error(str(e))
        if str(e) == 'Signature has expired' or str(e) == 'Signature verification failed':
            return Response("Phiên đăng nhập hết hạn hoặc không hợp lệ", status_code=401)
        else:
            return Response("Internal server error", status_code=500)


app.middleware('http')(catch_exceptions_middleware)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5000",
    "http://localhost:8080",
    "http://my.tiing.vn",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(promotions.router)
app.include_router(tasks.router)
app.include_router(staffs.router)
app.include_router(orders.router)
app.include_router(combo.router)
app.include_router(banners.router)
app.include_router(stores.router)
app.include_router(versions.router)
app.include_router(search.router)
app.include_router(location.router)
app.include_router(notifications.router)


@app.get("/")
async def root():
    return "housework"
