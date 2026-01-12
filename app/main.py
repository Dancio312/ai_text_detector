# -*- coding: utf-8 -*-

from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Text Detector")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"status": "API dziala"}
    
@app.get("/health")
def health():
    return {"status": "ok"}


