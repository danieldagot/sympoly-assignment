from datetime import datetime
from pydantic import BaseModel, EmailStr, Field,ConfigDict
from typing import List, Optional
from enum import Enum, IntEnum

class Reporter(BaseModel):
    model_config = ConfigDict(extra='forbid')
    fullname: str
    email: EmailStr
 
class Approver(BaseModel):
    model_config = ConfigDict(extra='forbid')
    fullname: str
    email: EmailStr
    approvalDate: Optional[datetime] = Field(None, alias='ApprovalDate')


class Transaction(BaseModel):
    model_config = ConfigDict(extra='forbid')
    data: str = Field(min_length=10, pattern=r"(\d{14})([CD])(\d+,\d{2})([A-Z]{3})")
    reference: str
    details : str
class StatusEnum(Enum):
    Draft = "0"
    Submitted = "1"
    Approved = "2"
    Rejected = "3"

class CurrencyEnum(Enum):
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    
class Details (BaseModel):
    model_config = ConfigDict(extra='forbid')
    createdat:str 
    status  : StatusEnum
    
class ReportDetails(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str 
    reporter: Reporter
    approvers: List[Approver]
    transactions: List[Transaction]
    details: Details
    


class MercuryEXRF(BaseModel):
    model_config = ConfigDict(extra='forbid')
    report: ReportDetails


