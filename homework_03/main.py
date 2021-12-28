# -*- coding: utf-8 -*-
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/ping/")
def read_ping():
    return {"message": "pong"}


@app.get("/time/")
def read_time():
    return {"time": datetime.now().strftime('%d.%m.%Y %H:%M:%S')}