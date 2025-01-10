from fastapi import APIRouter, HTTPException
from typing import Generic, TypeVar, List, Optional
from fastapi.params import Query
from pydantic import BaseModel

# Generic type for your model
T = TypeVar('T', bound=BaseModel)

class BaseRouter(Generic[T]):
    def __init__(
        self,
        model: T,
        prefix: str,
        tags: List[str],
        service = None  # Optional service class
    ):
        self.model = model
        self.router = APIRouter(prefix=prefix, tags=tags)
        self.service = service
        self._register_routes()

    def _register_routes(self):
        @self.router.get("/", response_model=List[self.model])
        async def get_all():
            if self.service:
                return await self.service.get_all()
            raise NotImplementedError()

        @self.router.get("", response_model=self.model)
        async def get_one(
            item_id: str = Query(..., description="ID of the product to retrieve")
        ):
            if self.service:
                return await self.service.get_one(item_id)
            raise NotImplementedError()

        @self.router.post("/", response_model=self.model)
        async def create(item: self.model):
            if self.service:
                return await self.service.create(item)
            raise NotImplementedError()

        @self.router.put("/{item_id}", response_model=self.model)
        async def update(item_id: str, item: self.model):
            if self.service:
                return await self.service.update(item_id, item)
            raise NotImplementedError()

        @self.router.delete("/{item_id}")
        async def delete(item_id: str):
            if self.service:
                return await self.service.delete(item_id)
            raise NotImplementedError()