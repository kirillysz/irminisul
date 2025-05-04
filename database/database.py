from async_appwrite.async_client import AsyncClient
from async_appwrite.services.async_databases import Databases

from utils.utils import Utils

class Database:
    def __init__(self, endpoint: str, project_id: str, api_key: str, 
                 database_id: str,
                 collection_id: str):
        self.client = AsyncClient()
        self.database = database_id
        self.collection = collection_id

        self.client.set_endpoint(endpoint=endpoint)
        self.client.set_project(value=project_id)
        self.client.set_key(value=api_key)
        self.client.set_self_signed()

        self.databases = Databases(client=self.client)


    async def add_data_to_collection(self, data: dict) -> dict:
        """Добавляет данные в коллекцию"""
        try:
            result = await self.databases.create_document(
                database_id=self.database,
                collection_id=self.collection,
                document_id=str(Utils.generate_id()),
                data=data
            )
            return result
        
        except Exception as err:
            raise Exception(err)
    
    async def get_data_by_id(self, document_id: str) -> dict:
        """Получает данные по ID"""
        try:
            result = await self.databases.get_document(
                database_id=self.database,
                collection_id=self.collection,
                document_id=document_id
            )
            return result
        
        except Exception as err:
            raise Exception(err)
    
