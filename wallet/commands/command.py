import uuid

from dataclasses import asdict
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from wallet.entities.wallet import (
    OperationType,
    Wallet,
)
from wallet.exceptions import WalletNotFoundApiError
from wallet.storages.wallet_storage import AbstractWalletRepository


class UpdateWalletRequestDTO(BaseModel):
    amount: Decimal
    operation_type: OperationType


class UpdateWalletResponse(BaseModel):
    balance: Decimal
    uuid: uuid.UUID
    updated_at: datetime


class UpdateWalletCommand:

    def __init__(self, wallet_repo: AbstractWalletRepository):
        self.wallet_repo = wallet_repo

    def execute(
        self, data: UpdateWalletRequestDTO, uuid: uuid.UUID
    ) -> UpdateWalletResponse:
        with self.wallet_repo.transaction():
            wallet = self.wallet_repo.get_by_uuid_or_none(uuid=uuid)
            if not wallet:
                wallet = self.wallet_repo.add(Wallet.create(wallet_uuid=uuid))

            wallet.update_balance(
                operation=data.operation_type, amount=data.amount
            )

            wallet = self.wallet_repo.update(wallet)
            return UpdateWalletResponse(**asdict(wallet))


class GetBalanceCommand:
    def __init__(self, wallet_repo: AbstractWalletRepository):
        self.wallet_repo = wallet_repo

    def execute(self, uuid: uuid):
        wallet = self.wallet_repo.get_by_uuid_or_none(uuid)
        balance = None
        if wallet:
            balance = {"balance": wallet.balance}
            return balance
        raise WalletNotFoundApiError()
