import abc
from peewee import * 
import uuid


from wallet.entities.wallet import Wallet


class BaseModel(Model):
    id = AutoField()

    class Meta:
        database = db



class Wallet_model(BaseModel):
    balance = FloatField()
    uuid = UUIDField()
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
    def from_query_to_object(self, query: Wallet_model)-> Wallet:
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