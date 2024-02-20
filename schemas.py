from datetime import datetime
from pydantic import BaseModel, EmailStr, Field,ConfigDict,computed_field
from typing import List, Optional
from enum import Enum, IntEnum
from datetime import datetime, timezone
from typing import Any, Dict
from typing_extensions import Annotated
from pydantic import BaseModel, WrapSerializer



class Reporter(BaseModel):
    model_config = ConfigDict(extra='forbid')
    fullname: str
    email: EmailStr
 
class Approver(BaseModel):
    model_config = ConfigDict(extra='forbid')
    fullname: str
    email: EmailStr
# class CurrencyEnum(Enum):
#     USD = 'USD'
#     EUR = 'EUR'
#     GBP = 'GBP'
    
class TransactionDataTypeEnum(Enum):
    debit = 'd'
    credit = 'c'

class DetailedTransactionData(BaseModel):
    date: datetime
    type: TransactionDataTypeEnum
    amount: float
    currency: str
class Transaction(BaseModel):
    model_config = ConfigDict(extra='forbid')
    data: str = Field(min_length=10, pattern=r"(\d{14})([CD])(\d+,\d{2})([A-Z]{3})")
    reference: str
    details : str

    def to_detailed_transaction_data(self) -> DetailedTransactionData:
        # Extracting components from the data field
        date_str, type_str, amount_str, currency_str = self.data[:14], self.data[14], self.data[15:-3], self.data[-3:]
        date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
        transaction_type = TransactionDataTypeEnum.credit if type_str == 'C' else TransactionDataTypeEnum.debit
        amount = float(amount_str.replace(',', '.'))
        currency = currency_str
        self.data = DetailedTransactionData(date=date, type=transaction_type, amount=amount, currency=currency)
        # return DetailedTransactionData(date=date, type=transaction_type, amount=amount, currency=currency)

class DetailedTransaction(Transaction):
    data = DetailedTransactionData 
class StatusEnum(Enum):
    Draft = "0"
    Submitted = "1"
    Approved = "2"
    Rejected = "3"

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
    invoice_id: Optional[str] = Field(None, alias='reportId')
    def to_detailed_transaction_data_report(self):
        [t.to_detailed_transaction_data() for t in self.transactions]
        return self
    
class DetailedReportDetails(ReportDetails):
    transactions: List[DetailedTransactionData]

class MercuryEXRF(BaseModel):
    model_config = ConfigDict(extra='forbid')
    report: ReportDetails
    def to_detailed_transaction_data_report(self):
        self.report.to_detailed_transaction_data_report()
        return self


    # create a new field wich is the last 3 characters of the data field
    # @computed_field
    # @property
    # def currency(self)->str:
    #     return self.data[-3:]
    # # create a new field wich is the amount of the data field
    # @computed_field
    # @property
    # def amount(self)->float:
    #     return float(self.data[15:-3].replace(',', '.'))
    # # create a new field wich is the date of the data field
    # @computed_field
    # @property
    # def date(self)->str:
    #     return self.data[:14]
    # @computed_field
    # @property
    # def type(self)->str:
    #     return self.data[14:15]