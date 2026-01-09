# -*- coding: utf-8 -*-

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI Text Detector")

app.include_router(router)

@app.get("/")
def root():
    return {"status": "API dziala"}
