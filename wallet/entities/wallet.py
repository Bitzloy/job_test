import uuid
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum

from wallet.exceptions import MoneyNotEnoughApiError



class OperationType(StrEnum):
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"



@dataclass
class Wallet():
    balance: Decimal
    uuid: uuid
    updated_at: datetime
    
    
    """метод создания тестового кошелька"""
    @classmethod
    def create(cls, balance: Decimal=Decimal(0), uuid=None) -> "Wallet":
        return cls(
            balance=balance,
            uuid=uuid or uuid.uuid4(),
            updated_at=datetime.now()
        )
       
    def deposit(self, amount: Decimal) -> None:
        self.balance += amount
        self.updated_at = datetime.now()
        
    
    def withdraw(self, amount: Decimal) -> None:
        self.balance -= amount
        self.updated_at = datetime.now()
        
    
    def update_balance(self, operation: OperationType, amount: Decimal):
    
        if operation == OperationType.WITHDRAW: #ccылка на тип из enum
            # if wallet.balance >= UpdateWalletRequest.amount:
            if self.balance < amount:
                raise MoneyNotEnoughApiError()
            
            self.withdraw(amount)
            
        elif operation == OperationType.DEPOSIT:
            self.deposit(amount)
            