from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.ml.model import load_model


app = FastAPI(title="AI Text Detector API")

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Startup hook ===
@app.on_event("startup")
def load_models_on_startup():
    load_model()

# === Routes ===
app.include_router(router)
