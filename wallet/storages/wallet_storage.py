import abc
import uuid

from peewee import *

from wallet.database import make_db
from wallet.entities.wallet import Wallet


class BaseModel(Model):
    id = AutoField()

    class Meta:
        database = make_db()


class Wallet_model(BaseModel):
    balance = DecimalField()
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
    def get_by_uuid_or_none(self, uuid: uuid.UUID) -> Wallet | None:
        pass

    @abc.abstractmethod
    def from_query_to_wallet(self, query: Wallet_model) -> Wallet:
        pass

    @abc.abstractmethod
    def delete(self, uuid: uuid.UUID) -> None:
        pass

    @abc.abstractmethod
    def transaction():
        pass


class OrmWalletRepo(AbstractWalletRepository):

    def __init__(self, connect: PostgresqlDatabase):
        self.connect = connect

    def add(self, wallet: Wallet) -> Wallet:
        added_wallet = Wallet_model.create(
            balance=wallet.balance,
            uuid=wallet.uuid,
            updated_at=wallet.updated_at,
        )
        return self.from_query_to_wallet(query=added_wallet)

    def update(self, wallet: Wallet) -> Wallet:
        Wallet_model.update(
            balance=wallet.balance, updated_at=wallet.updated_at
        ).where(Wallet_model.uuid == wallet.uuid).execute()

        return wallet

    def get_by_uuid_or_none(self, uuid: uuid.UUID) -> Wallet | None:

        wallet = Wallet_model.get_or_none(Wallet_model.uuid == uuid)
        if not wallet:
            return None

        return self.from_query_to_wallet(wallet)

    def from_query_to_wallet(self, query: Wallet_model) -> Wallet:
        wallet = Wallet(
            balance=query.balance, uuid=query.uuid, updated_at=query.updated_at
        )

        return wallet

    def delete(self, uuid):
        model_to_delete = Wallet_model.get_or_none(Wallet_model.uuid == uuid)
        if model_to_delete:
            model_to_delete.delete_instance()

    # @contextmanager
    # def transaction(self, isolation_level):
    #     conn = db.connection()
    #     conn.set_isolation_level(isolation_level)
    #     try:
    #         with db.atomic():
    #             yield
    #     finally:
    #         conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)

    def transaction(self):
        return self.connect.atomic()
