from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from exrf import extract_data_from_exrf_string
import schemas
app = FastAPI()


@app.post("/invoices/")
async def upload_invoice(file: UploadFile):
    content = await file.read()
    content = content.decode("utf-8")
    print(content)
    data = extract_data_from_exrf_string(content)
    print(data)
    exrf_instance = schemas.MercuryEXRF(**data)
    return exrf_instance
    # Here, parse the file content, convert it to the MercuryEXRF model, and save to MongoDB
    # This is a placeholder for parsing logic
    # parsed_data = {}  # Replace with actual parsing logic
    # invoice = Invoice(**parsed_data)
    # await invoice.save()
    # return parsed_data

# @app.get("/invoices/")
# async def get_invoices():
#     invoices = await Invoice.find_all().to_list()
#     return invoices

# @app.get("/invoices/{invoice_id}")
# async def get_invoice(invoice_id: str):
#     invoice = await Invoice.get(invoice_id)
#     if invoice is None:
#         raise HTTPException(status_code=404, detail="Invoice not found")
#     return invoice

# @app.delete("/invoices/{invoice_id}")
# async def delete_invoice(invoice_id: str):
#     await Invoice.find_one(Invoice.id == invoice_id).delete()
#     return {"message": "Invoice deleted successfully"}
# 
    

    # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )extract_data Beanie 

# @app.on_event("startup")
# async def startup_event():
#     await init()  # Initialize Beanie with MongoDB
