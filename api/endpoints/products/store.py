from api.endpoints.products._product_router import BaseRouter
from schemas.products import Product
from services.product_service import BaseProductService


class StoreService(BaseProductService):
    async def get_one(self, item_id: str):
        return Product(id=item_id, name="Store", price=100.0, description="Test Store product")
    
    async def get_Store_data(self, item_id: str):
        return Product(id=item_id, name="Store", price=100.0, description="Test Store product")

    async def get_all(self):
        # Implement get all products logic
        return []

    async def create(self, data: Product):
        # Implement create product logic
        return data

    async def update(self, item_id: str, data: Product):
        # Implement update product logic
        return data

    async def delete(self, item_id: str):
        # Implement delete product logic
        return True



class StoreRouter(BaseRouter[Product]):
    def __init__(self):
        super().__init__(
            model=Product,
            prefix="/Store",
            tags=["Store"],
            service=StoreService()
        )
        self.add_custom_routes()

    def add_custom_routes(self):
        @self.router.get(
            "/custom", 
            response_model=dict,
            include_in_schema=True,
            response_description="Custom route response"
        )
        async def custom_route():
            try:
                print("Custom route accessed!")
                return {"message": "This is a custom route"}
            except Exception as e:
                print(f"Error in custom route: {str(e)}")
                raise
        
    


store_router = StoreRouter()