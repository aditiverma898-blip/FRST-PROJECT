import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
import logging

from .routes import router
from .errors import validation_exception_handler, generic_exception_handler
from data.loader import get_dataframe as load_dataset
from data.preprocessor import clean_dataframe as preprocess_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state for dataset
app_state = {"df": None}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Loading Zomato dataset...")
    try:
        app_state["df"] = load_dataset()
        logger.info(f"Dataset loaded with {len(app_state['df'])} records.")
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
    yield
    # Shutdown
    app_state["df"] = None

def create_app() -> FastAPI:
    app = FastAPI(
        title="Zomato AI Recommendations API",
        description="REST API for Zomato AI-powered restaurant recommendations",
        version="1.0.0",
        lifespan=lifespan
    )

    # CORS
    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in cors_origins],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # Routes
    app.include_router(router, prefix="/api/v1")

    return app

app = create_app()
