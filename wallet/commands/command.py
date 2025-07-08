from pydantic import BaseModel, Field
import uuid
from wallet.entities.wallet import Wallet
from wallet.storages.wallet_storage import AbstractWalletRepository


"""
При переходе по несуществующему uuid в зависимости от операции, кидаем исключение или создаем новый кошелек
В данном случае создаем, так как операция пополнение
"""   

class UpdateWalletCommand():
    
    def __init__(self, operation, amount, wallet:Wallet):
        self.operation = operation
        self.amount = amount
        self.wallet = wallet
        
    
    def execute(self, uuid:uuid, wallet_repo: AbstractWalletRepository):
        wallet = wallet_repo.get_by_uuid_or_none(uuid=uuid)
        if wallet:
            if self.operation == "WITHDRAW":
                if wallet.balance >= self.amount:
                    wallet.withdraw(self.amount)
                    return wallet_repo.update(wallet)
                raise Exception()
            
            elif self.operation == "DEPOSIT":
                wallet.deposit(self.amount)
                return wallet_repo.update(wallet)
            
        return self.is_not_exist(uuid, wallet_repo)
    
    
    
    def is_not_exist(self, uuid:uuid, wallet_repo: AbstractWalletRepository):
        if self.operation == "WITHDRAW":
            raise Exception()
        
        elif self.operation == "DEPOSIT":
            new_wallet = self.wallet.create(id=uuid)
            new_wallet.deposit(self.amount)
            return wallet_repo.add(new_wallet)



class GetBalanceCommand():
    
    def execute(self, uuid: uuid, wallet_repo: AbstractWalletRepository):
        wallet = wallet_repo.get_by_uuid_or_none(uuid)
        balance = None
        if wallet:
            balance = {"balance": wallet.balance}
            return balance
        raise Exception()