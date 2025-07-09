from pydantic import BaseModel, field_validator, ValidationError
import uuid
from wallet.entities.wallet import Wallet, OperationType
from wallet.storages.wallet_storage import AbstractWalletRepository
from wallet.exceptions import WalletNotFoundApiError, MoneyNotEnoughApiError
from decimal import Decimal

"""
При переходе по несуществующему uuid в зависимости от операции, кидаем исключение или создаем новый кошелек
В данном случае создаем, так как операция пополнение
"""   

class UpdateWalletRequestDTO(BaseModel):
    amount: Decimal
    operation_type: OperationType
    
    
    # @field_validator("amount", mode="before")
    # def check_fields(cls, value):
    #     if not isinstance(value, Decimal):
    #         raise ValueError("oshibka")
    #     return value
    

class UpdateWalletCommand():
    
    def __init__(self, wallet_repo: AbstractWalletRepository):
        self.wallet_repo = wallet_repo
        
    
    def execute(self, data: UpdateWalletRequestDTO, uuid: uuid.UUID):
        with self.wallet_repo.transaction() as transaction:
            wallet = self.wallet_repo.get_by_uuid_or_none(uuid=uuid)
            if not wallet:
                wallet = self.wallet_repo.add(Wallet.create(uuid=uuid))
                
            wallet.update_balance(
                operation=data.operation_type, 
                amount=data.amount
                )
            
            return self.wallet_repo.update(wallet)
            



class GetBalanceCommand():
    def __init__(self, wallet_repo: AbstractWalletRepository):
        self.wallet_repo = wallet_repo
    
    def execute(self, uuid: uuid):
        wallet = self.wallet_repo.get_by_uuid_or_none(uuid)
        balance = None
        if wallet:
            balance = {"balance": wallet.balance}
            return balance
        raise WalletNotFoundApiError()