from fastapi import APIRouter, UploadFile

import schemas
router = APIRouter() 
from exrf import extract_data_from_exrf_string

@router.post("")
async def upload_invoice(file: UploadFile ):
    content = await file.read()
    content = content.decode("utf-8")
    print(content)
    data = extract_data_from_exrf_string(content)
    print(data)
    exrf_instance = schemas.MercuryEXRF(**data)
    return exrf_instance