from async_appwrite.async_client import AsyncClient
from async_appwrite.services.async_storage import AsyncStorage

from appwrite.input_file import InputFile

from utils.utils import Utils


class Storage:
    def __init__(self, bucket_id: str, endpoint: str, project_id: str, api_key: str,):
        self.client = AsyncClient()
        self.client.set_endpoint(endpoint=endpoint)
        self.client.set_project(value=project_id)
        self.client.set_key(value=api_key)
        self.client.set_self_signed()

        self.bucket_id = bucket_id
        self.storage = AsyncStorage(client=self.client)

    async def upload(self, file_path: str) -> dict[str: str]:
        """Загрузка файла в Хранилище"""
        file = InputFile.from_path(path=file_path)

        result = await self.storage.create_file(
            bucket_id=self.bucket_id,
            file_id=Utils.generate_id(),
            file=file
        )
            
        return result
