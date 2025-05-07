from fastapi import APIRouter, Form, UploadFile, File, Request, HTTPException
from fastapi.responses import RedirectResponse

from starlette.status import HTTP_303_SEE_OTHER

from json import dumps
from typing import List

from database.database import Database
from storage.storage import Storage

from utils.utils import Utils
from config import Config

import os

router = APIRouter(prefix="/data")
cfg = Config()

db = Database(
    endpoint=cfg.ENDPOINT,
    project_id=cfg.PROJECT_ID,
    api_key=cfg.DB_KEY,
    database_id=cfg.DATABASE_ID,
    collection_id=cfg.COLLECTION_ID
)

storage = Storage(
    bucket_id=cfg.BUCKET_ID,
    endpoint=cfg.ENDPOINT,
    project_id=cfg.PROJECT_ID,
    api_key=cfg.DB_KEY
)

@router.post("/work-save")
async def submit_work(
    request: Request,
    g_recaptcha_response: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    institution: str = Form(...),
    specialty: str = Form(...),
    course: int = Form(...),
    work_type: str = Form(...),
    subject: str = Form(...),
    keywords: str = Form(""),
    date: str = Form(""),
    username: str = Form(...),
    file: List[UploadFile] = File(...)
):
    is_valid_captcha = await Utils.verify_captcha(response = g_recaptcha_response)
    if not is_valid_captcha:
        raise HTTPException(status_code=400, detail="reCAPTCHA verification failed")

    os.makedirs(cfg.UPLOAD_DIR, exist_ok=True)
    file_ids = []
    
    if len(file) > 10:
        raise HTTPException(status_code=400, detail="Превышен максимальный лимит для файлов (10)")

    for uploaded_file in file:
        file_path = os.path.join(cfg.UPLOAD_DIR, uploaded_file.filename)

        with open(file_path, "wb") as buffer:
            content = await uploaded_file.read()
            buffer.write(content)

        try:
            result = await storage.upload(file_path=file_path)
            file_ids.append(result["$id"])

        finally:
            if os.path.exists(file_path):
                os.remove(file_path)


    data = dumps(
        {
            "id": Utils.generate_id(),
            "title": title,
            "description": description,
            "institution": institution,
            "specialty": specialty,
            "course": course,
            "work_type": work_type,
            "subject": subject,
            "keywords": keywords.split(","),
            "work_date": date,
            "username": username,
            "file_ids": file_ids
        }
    )

    try:
        await db.add_data_to_collection(data=data)
        return RedirectResponse(url="https://irminsul.space/?success=1", status_code=HTTP_303_SEE_OTHER)
    
    except Exception:
        return RedirectResponse(url="https://irminsul.space/?error=1", status_code=HTTP_303_SEE_OTHER)