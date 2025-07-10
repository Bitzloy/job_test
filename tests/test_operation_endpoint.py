import uuid


def test_deposit_end_point(client, create_wallet, wallet_repo):
    wallet = create_wallet

    response = client.post(
        f"/api/v1/wallets/{wallet.uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000},
    )

    json_response = response.json

    assert isinstance(uuid.UUID(json_response["uuid"]), uuid.UUID)
    assert json_response["balance"] == f"{wallet.balance + 1000}.00000"
    assert "updated_at" in json_response
    assert response.status_code == 200

    wallet_repo.delete(json_response["uuid"])


def test_withdraw_end_point(client, create_wallet, wallet_repo):
    wallet = create_wallet

    response = client.post(
        f"/api/v1/wallets/{wallet.uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": 1000},
    )

    json_response = response.json

    assert isinstance(uuid.UUID(json_response["uuid"]), uuid.UUID)
    assert json_response["balance"] == f"{wallet.balance - 1000}.00000"
    assert "updated_at" in json_response
    assert response.status_code == 200

    wallet_repo.delete(json_response["uuid"])


"""
При переходе по несуществующему uuid в зависимости от операции, кидаем исключение или создаем новый кошелек
В данном случае создаем, так как операция пополнение
"""


def test_deposit_not_existable_wallet(client, wallet_repo):

    response = client.post(
        f"/api/v1/wallets/{uuid.uuid4()}/operation",
        json={"operation_type": "DEPOSIT", "amount": 1000},
    )

    json_response = response.json

    assert isinstance(uuid.UUID(json_response["uuid"]), uuid.UUID)
    assert json_response["balance"] == str(1000)
    assert "updated_at" in json_response
    assert response.status_code == 200

    wallet_repo.delete(json_response["uuid"])


def test_withdraw_not_enough_money(client):
    response = client.post(
        f"/api/v1/wallets/{uuid.uuid4()}/operation",
        json={"operation_type": "WITHDRAW", "amount": 1000},
    )

    assert response.status_code == 403
    assert "MONEY_NOT_ENOUGH" in response.json["code"]


def test_get_balance(client, create_wallet, wallet_repo):
    wallet = create_wallet

    response = client.get(f"/api/v1/wallets/{wallet.uuid}/")
    json_response = response.json

    assert json_response == {"balance": f"{wallet.balance}.00000"}

    wallet_repo.delete(uuid=wallet.uuid)


def test_get_not_exist_wallet(client):
    response = client.get(f"/api/v1/wallets/{uuid.uuid4()}/")

    assert response.status_code == 404
    assert response.json["code"] == "WALLET_NOT_FOUND"
