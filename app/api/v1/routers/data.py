from fastapi import APIRouter, Form, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from json import dumps
from typing import List

from database.database import Database
from storage.storage import Storage

from utils.utils import Utils
from config import Config

import os

router = APIRouter(prefix="/data")
cfg = Config()
templates = Jinja2Templates(directory="templates/")


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
        result = await db.add_data_to_collection(data=data)
        return templates.TemplateResponse("index.html", {"request": request, "success": True})
    
    except Exception:
        return templates.TemplateResponse("index.html", {"request": request, "error": True})
