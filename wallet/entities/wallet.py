import uuid
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Wallet():
    balance: float
    uuid: uuid
    updated_at: datetime
    
    
    """метода создания тестового кошелька"""
    @classmethod
    def create(cls, balance: float) -> "Wallet":
        return cls(
            balance=balance,
            uuid=uuid.uuid4(),
            updated_at=datetime.now()
        )
       
    def deposit(self, amount: float) -> None:
        self.balance += amount
        self.updated_at = datetime.now()
        
    
    def withdraw(self, amount: float) -> None:
        self.balance -= amount
        self.updated_at = datetime.now()
        