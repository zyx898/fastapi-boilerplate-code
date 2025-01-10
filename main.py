# Python standard library imports
import os
import sys
from contextlib import asynccontextmanager

# Third-party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Local imports
from core.config import settings
from api.router import api_routers
from core.loggerConfig import setup_logger
from core.initialization import initialize_app, uninitialize_app

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


logger = setup_logger(__name__, settings.LOG_FILE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await initialize_app()
    yield
    # Shutdown (if needed)
    await uninitialize_app()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=f"API for {settings.PROJECT_NAME}",
    redoc_url="/docs",
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the exact origin
    allow_credentials=True,  # Allow credentials
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


app.include_router(api_routers)
