from aiohttp import ClientSession
from uuid import uuid4

from json import dumps
from config import Config

cfg = Config()

class Utils:
    @staticmethod
    def generate_id() -> str:
        """Генерация уникального UUID"""
        return str(uuid4())

    @staticmethod
    async def verify_captcha(response: str) -> bool:
        """Проверка reCAPTCHA v2"""
        async with ClientSession() as session:
            async with session.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data=dumps({
                    "secret": cfg.RECAPTCHA_SECRET,
                    "response": response
                })
            ) as resp:
                result = await resp.json()
                return result.get("success", False)