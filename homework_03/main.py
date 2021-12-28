# -*- coding: utf-8 -*-
from fastapi import FastAPI, status
from datetime import datetime

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ping/", status_code=status.HTTP_200_OK)
def read_ping():
    return {"message": "pong"}


@app.get("/time/")
def read_time():
    return {"time": datetime.now().strftime('%d.%m.%Y %H:%M:%S')}