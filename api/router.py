import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter
from .endpoints.products.store import store_router

api_routers = APIRouter()

api_routers.include_router(store_router.router)
