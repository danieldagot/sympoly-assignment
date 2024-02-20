import json
from fastapi import APIRouter, UploadFile, HTTPException
from pydantic import ValidationError
from database import Invoice  # Adjust import path as necessary
# import schemas 
from models.invoiceModel import  MercuryEXRF 
from models.invoiceModelDetailed import  DetailedReportDetails 
from pprint import pprint
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
        mercury_exrf_instance = MercuryEXRF(**data)
        return mercury_exrf_instance
    except Exception as e:
        # Handle exceptions, such as validation errors or database connection issues
        # if the error is a validation error, return a 422 status code with the validation error details
        if isinstance(e, ValidationError):
            raise HTTPException(status_code=422, detail=e.json())



@router.post("/test")  # Ensure you have a valid path here
async def upload_invoice(file: UploadFile ):
    # TODO: Add validation for the file type
    # TODO : valdated that invoice_id is unique 
    content = await file.read()
    content = content.decode("utf-8")
    data = extract_data_from_exrf_string(content)
    mercury_exrf_instance = validate_mercury_exrf(data)
    mercury_exrf_instance = mercury_exrf_instance.to_detailed_transaction_data_report() 
    
    report =  mercury_exrf_instance.report.model_dump()
    
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
    
    # return report 
    # try:
        
    #     # add logging to report with json 
    #     pprint(report)


    #     # return  DetailedReportDetails(**report)

    # except ValidationError as e:
    #     for error in e.errors():
    #         failed_value = get_nested_value(data, error['loc'])  # Assuming 'data' is the original input data dictionary
    #         print(f"Error in field {error['loc']}: {error['msg']}, failed value: {failed_value}")

     
    # return mercury_exrf_instance.report.to_detailed_transaction_data_report()
    # try:
    #     invoice_instance = Invoice(**report)
    #     pprint
    #     return invoice_instance 
    # except Exception as e:
    #     if isinstance(e, ValidationError):
    #         raise HTTPException(status_code=422, detail=e.json())
    #     raise HTTPException(status_code=500, detail=f"Failed to save invoice data: {str(e)}")
    

def get_nested_value(data, loc):
    """Recursively fetch the value from nested dictionaries/lists based on loc."""
    for loc_part in loc:
        if isinstance(data, dict):
            data = data.get(loc_part)
        elif isinstance(data, (list, tuple)):
            data = data[loc_part] if len(data) > loc_part else None
        else:
            return None  # Not a dict or list, or path is incorrect
    return data
