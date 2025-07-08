import abc
from peewee import * 
import uuid


from wallet.entities.wallet import Wallet

from wallet.database import db


class BaseModel(Model):
    id = AutoField()

    class Meta:
        database = db



class Wallet_model(BaseModel):
    balance = DecimalField()
    uuid = CharField()
    updated_at = CharField()
    
    class Meta:
        table_name = "wallet"
        order_by = "updated_at"
        
        

class AbstractWalletRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, wallet: Wallet) -> Wallet:
        pass
    
    
    @abc.abstractmethod
    def update(self, wallet: Wallet) -> Wallet:
        pass
    
    @abc.abstractmethod
    def get_by_id_or_none(self, uuid: uuid.UUID) -> Wallet | None:
        pass
    
    @abc.abstractmethod
    def from_query_to_wallet(self, query: Wallet_model)-> Wallet:
        pass
    
    @abc.abstractmethod
    def delete(self, uuid: uuid.UUID) -> None:
        pass
    

class OrmWalletRepo(AbstractWalletRepository):
    
    def add(self, wallet: Wallet)-> Wallet:
        added_wallet = Wallet_model.create(
            balance=wallet.balance,
            uuid=wallet.uuid,
            updated_at=wallet.updated_at
            
        )
        return self.from_query_to_wallet(query=added_wallet)
    
    
    def update(self, wallet: Wallet)-> Wallet:
        Wallet_model.update(
            balance=wallet.balance,
            updated_at=wallet.updated_at
        ).where(Wallet_model.uuid == wallet.uuid).execute()
        
        return wallet
    
    
    def get_by_id_or_none(self, uuid: uuid.UUID) -> Wallet | None:
        
        model = Wallet_model.get_or_none(Wallet_model.uuid == uuid)
        if not model:
            return None
        
        return self.from_query_to_wallet(model)
    
    
    def from_query_to_wallet(self, query: Wallet_model)-> Wallet:
        wallet = Wallet(balance=query.balance, 
                        uuid=query.uuid, 
                        updated_at=query.updated_at)
        
        return wallet
    
    
    def delete(self, uuid):
        model_to_delete = Wallet_model.get_or_none(Wallet_model.uuid == uuid)
        if model_to_delete:
            model_to_delete.delete_instance()
        # Wallet_model.delete(Wallet_model.where Wallet_model.uuid == uuid)
        # Wallet_model.delete((Wallet_model.balance, Wallet_model.updated_at, Wallet_model,uuid).where(Wallet_model.uuid == uuid))