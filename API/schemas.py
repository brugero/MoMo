from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    FullNames: str
    PhoneNumber: str

class User(UserCreate):
    UserId: int
    DateCreated: Optional[str] = None

class TransactionCategoryCreate(BaseModel):
    TransactionType: str
    paymentType: str

class TransactionCategory(TransactionCategoryCreate):
    categoryId: int

class TransactionCreate(BaseModel):
    Fee: float = 0.0
    Amount: float
    balance: float
    initialBalance: float
    senderUserId: int
    receiverUserId: int
    transactionDate: Optional[str] = None 
    categoryId: int
    TransactionReference: Optional[str] = None

class Transaction(TransactionCreate):
    TransactionId: int

class SystemLogCreate(BaseModel):
    status: str
    transactionId: Optional[int] = None
    timestamp: Optional[str] = None

class SystemLog(SystemLogCreate):
    logId: str