from typing import List
import json
from fastapi import APIRouter, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from database import Invoice
from models.invoceResponceModel import InvoiceResponse  # Adjust import path as necessary
# import schemas 
from models.invoiceModel import  MercuryEXRF 
from models.invoiceModelDetailed import  DetailedReportDetails 
from pprint import pprint
from exrf import extract_data_from_exrf_string  # Adjust import path as necessary
from fastapi.encoders import jsonable_encoder 
router = APIRouter()
import logging

logging.basicConfig(filename='app2.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@router.post("")  # Adjust the path as necessary
async def upload_invoice(file: UploadFile):
    logging.info("Attempting to upload file: %s", file.filename)
    file_name = file.filename
    if not file_name.endswith(".exrf"):
        logging.warning("Attempted to upload an invalid file type: %s", file_name)
        raise HTTPException(status_code=422, detail="Invalid file type. Only .exrf files are allowed.")
    
    try:
        content = await file.read()
        content = content.decode("utf-8")
        data = extract_data_from_exrf_string(content)
        mercury_exrf_instance = validate_mercury_exrf(data)
        report_details = mercury_exrf_instance.to_detailed_transaction_data_report()
        report = report_details.report.model_dump()
        report["invoice_id"] = report["id"]
        del report["id"]

        invoice_data = await Invoice.find_one(Invoice.invoice_id == report["invoice_id"])
        if invoice_data:
            logging.warning("Invoice with id %s already exists.", report['invoice_id'])
            raise HTTPException(status_code=400, detail=f"Invoice with id {report['invoice_id']} already exists.")

        invoice_instance = Invoice(**report)
        await invoice_instance.save()
        logging.info("Successfully saved invoice: %s", report["invoice_id"])
        return invoice_instance

    except Exception as e:
        logging.error("Failed to process and save invoice: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Failed to process and save invoice: {str(e)}")
#  create get all invoices route
    
@router.get("" , response_model=List[InvoiceResponse])
async def get_invoices():
    invoices = await Invoice.find_all().to_list()
    return [invoice.dict(exclude={"_id"}) for invoice in invoices]

# create get invoice by id route
@router.get("/{invoice_id}" , response_model=InvoiceResponse)
async def get_invoice(invoice_id: str):
    invoiceData = await Invoice.find_one(Invoice.invoice_id == invoice_id)
    if invoiceData:
        return invoiceData
    raise HTTPException(status_code=404, detail="Invoice not found")



@router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: str):
    invoiceData = await Invoice.find_one(Invoice.invoice_id == invoice_id)
    if invoiceData:
        await invoiceData.delete()
        return {"message": "Invoice deleted successfully"}
    raise HTTPException(status_code=404, detail="Invoice not found")

def validate_mercury_exrf(data):
    # try:
    mercury_exrf_instance = MercuryEXRF(**data)
    return mercury_exrf_instance

