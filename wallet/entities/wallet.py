import uuid
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Wallet():
    balance: Decimal
    uuid: uuid
    updated_at: datetime
    
    
    """метода создания тестового кошелька"""
    @classmethod
    def create(cls, balance: Decimal=Decimal(0), id=None) -> "Wallet":
        return cls(
            balance=balance,
            uuid=id or uuid.uuid4(),
            updated_at=datetime.now()
        )
       
    def deposit(self, amount: Decimal) -> None:
        self.balance += Decimal(amount)
        self.updated_at = datetime.now()
        
    
    def withdraw(self, amount: Decimal) -> None:
        self.balance -= Decimal(amount)
        self.updated_at = datetime.now()
        