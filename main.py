from fastapi import FastAPI, UploadFile, HTTPException 
from exrf import extract_data_from_exrf_string
from database import init as init_db  # Adjust import as necessary
from routes import router as api_router
app = FastAPI()
@app.on_event("startup")
async def startup_event():
    await init_db()
app.include_router(api_router)


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
    
# @app.on_event("startup")
# async def startup_event():
#     await init()  # Initialize Beanie with MongoDB

