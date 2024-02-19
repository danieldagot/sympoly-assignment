from datetime import datetime
from pydantic import BaseModel, EmailStr, Field,ConfigDict,computed_field
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
    # create a new field wich is the last 3 characters of the data field
    @computed_field
    @property
    def currency(self)->str:
        return self.data[-3:]
    # create a new field wich is the amount of the data field
    @computed_field
    @property
    def amount(self)->float:
        return float(self.data[15:-3].replace(',', '.'))
    # create a new field wich is the date of the data field
    @computed_field
    @property
    def date(self)->str:
        return self.data[:14]
    @computed_field
    @property
    def type(self)->str:
        return self.data[14:15]
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


