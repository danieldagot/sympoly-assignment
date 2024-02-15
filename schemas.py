from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from enum import Enum, IntEnum

class Reporter(BaseModel):
    FullName: str
    Email: EmailStr
 
class Approver(BaseModel):
    FullName: str
    Email: EmailStr
    ApprovalDate: Optional[datetime] = Field(None, alias='ApprovalDate')


class Transaction(BaseModel):
    Data: str = Field(min_length=10, pattern=r"(\d{14})([CD])(\d+,\d{2})([A-Z]{3})")
    Reference: str
    Details : str
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
    CreatedAt:str 
    Status  : StatusEnum
class ReportDetails(BaseModel):
    ID :  str
    Reporter: Reporter
    Approvers: List[Approver]
    Transactions: List[Transaction]
    Details : Details



class MercuryEXRF(BaseModel):
    
    Report: ReportDetails

