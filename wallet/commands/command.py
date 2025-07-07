from pydantic import BaseModel, Field
import uuid
from wallet.entities.wallet import Wallet
from wallet.storages.wallet_storage import AbstractWalletRepository


class UpdateWalletCommand():
    
    def __init__(self, operation, amount, wallet: Wallet):
        self.operation = operation
        self.amount = amount
        self.wallet = wallet
        
    
    def execute(self, uuid:uuid, wallet_repo: AbstractWalletRepository):
        if wallet_repo.get_by_id_or_none(uuid):
            if self.operation == "withdraw":
                if self.wallet.balance >= self.amount:
                    self.wallet.withdraw(self.amount)
                    return wallet_repo.update(self.wallet)
                raise Exception()
            
            elif self.operation == "deposit":
                self.wallet.deposit(self.amount)
                return wallet_repo.update(self.wallet)
        raise Exception()