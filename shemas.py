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
    Date: datetime
    Amount: float
    Currency: str
    Description: str
class StatusEnum(IntEnum):
    Draft = 0
    Submitted = 1
    Approved = 2 
    Rejected = 3

class CurrencyEnum(Enum):
    USD = 'USD'
    EUR = 'EUR'
    GBP = 'GBP'
    
class ReportDetails(BaseModel):
    CreatedAt: datetime
    Status: StatusEnum
    TotalAmount: float
    Currency: CurrencyEnum


class MercuryEXRF(BaseModel):
    Report: ReportDetails
    Reporter: Reporter
    Approvers: List[Approver]
    Transactions: List[Transaction]
