import pytest
from decimal import Decimal


from wallet.__init__ import create_app
from wallet.storages.wallet_storage import OrmWalletRepo
from wallet.entities.wallet import Wallet


@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def wallet_repo():
    return OrmWalletRepo()


@pytest.fixture
def create_wallet(wallet_repo, balance: Decimal=Decimal(3000)):
    test_wallet = Wallet.create(balance=balance)
    added_wallet = wallet_repo.add(test_wallet)
    return added_wallet
    