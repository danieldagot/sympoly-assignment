from fastapi import APIRouter, UploadFile, HTTPException
from pydantic import ValidationError
from database import Invoice  # Adjust import path as necessary
import schemas
from exrf import extract_data_from_exrf_string  # Adjust import path as necessary

router = APIRouter()
import logging
@router.post("" ,response_model= Invoice )  # Ensure you have a valid path here
async def upload_invoice(file: UploadFile ):
    # TODO: Add validation for the file type
    # TODO : valdated that invoice_id is unique 
    content = await file.read()
    content = content.decode("utf-8")
    data = extract_data_from_exrf_string(content)
    mercury_exrf_instance = validate_mercury_exrf(data)
    report =  mercury_exrf_instance.report.dict()
    report["invoice_id"] = report["id"]

    del report["id"]
    try:
        invoiceData = await Invoice.find_one(Invoice.invoice_id == report["invoice_id"])
        if invoiceData:
            raise HTTPException(status_code=401, detail=f"Invoice with id {report['invoice_id']} already exists.")
        invoice_instance = Invoice(**report)
        logging.info(invoice_instance)
        await invoice_instance.save() 
        return invoice_instance  
    except Exception as e:
        if isinstance(e, ValidationError):
            raise HTTPException(status_code=422, detail=e.json())
        raise HTTPException(status_code=500, detail=f"Failed to save invoice data: {str(e)}")
    
#  create get all invoices route
@router.get("/")
async def get_invoices():
    invoices = await Invoice.find_all().to_list()
    return invoices

# create get invoice by id route
@router.get("/{invoice_id}")
async def get_invoice(invoice_id: str):
    invoiceData = await Invoice.find_one(Invoice.invoice_id == invoice_id)
    if invoiceData:
        return invoiceData
    raise HTTPException(status_code=404, detail="Invoice not found")
# create delete invoice by id route
@router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: str):
    invoiceData = await Invoice.find_one(Invoice.invoice_id == invoice_id)
    if invoiceData:
        await invoiceData.delete()
        return {"message": "Invoice deleted successfully"}
    raise HTTPException(status_code=404, detail="Invoice not found")
def validate_mercury_exrf(data):
    try:
        mercury_exrf_instance = schemas.MercuryEXRF(**data)
        return mercury_exrf_instance
    except Exception as e:
        # Handle exceptions, such as validation errors or database connection issues
        # if the error is a validation error, return a 422 status code with the validation error details
        if isinstance(e, ValidationError):
            raise HTTPException(status_code=422, detail=e.json())
