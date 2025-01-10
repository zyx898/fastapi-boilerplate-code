from abc import ABC, abstractmethod
from schemas.products import Product

class BaseProductService(ABC):
    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_one(self, item_id: str):
        pass

    @abstractmethod
    async def create(self, item: Product):
        pass

    @abstractmethod
    async def update(self, item_id: str, item: Product):
        pass

    @abstractmethod
    async def delete(self, item_id: str):
        pass
