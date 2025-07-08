import pytest
import uuid
import datetime


from wallet.storages.wallet_storage import OrmWalletRepo


def test_deposit_end_point(client, create_wallet, wallet_repo):
    wallet = create_wallet

    
    response = client.post(f"/api/v1/wallets/{wallet.uuid}/operation", 
                           json={"operation_type": "DEPOSIT", "amount": 1000})
    
    json_response = response.json
    
    
    assert isinstance(uuid.UUID(json_response["uuid"]), uuid.UUID)
    assert json_response["balance"] == str(wallet.balance + 1000)
    assert "updated_at" in  json_response 
    assert response.status_code == 200
    
    
    wallet_repo.delete(json_response["uuid"])



def test_withdraw_end_point(client, create_wallet, wallet_repo):
    wallet = create_wallet

    
    response = client.post(f"/api/v1/wallets/{wallet.uuid}/operation", 
                           json={"operation_type": "WITHDRAW", "amount": 1000})
    
    json_response = response.json
    
    
    assert isinstance(uuid.UUID(json_response["uuid"]), uuid.UUID)
    assert json_response["balance"] == str(wallet.balance - 1000)
    assert "updated_at" in  json_response 
    assert response.status_code == 200
    
    wallet_repo.delete(json_response["uuid"])

    
"""
При переходе по несуществующему uuid в зависимости от операции, кидаем исключение или создаем новый кошелек
В данном случае создаем, так как операция пополнение
"""    
def test_deposit_not_existable_wallet(client, wallet_repo):
        

        
    response = client.post(f"/api/v1/wallets/{uuid.uuid4()}/operation", 
                        json={"operation_type": "DEPOSIT", "amount": 1000})
    
    json_response = response.json
    
    print(json_response)
    assert isinstance(uuid.UUID(json_response["uuid"]), uuid.UUID)
    assert json_response["balance"] == str(1000)
    assert "updated_at" in  json_response 
    assert response.status_code == 200
    
    wallet_repo.delete(json_response["uuid"])
    

"""
В данном случае кидаем ошибку, так как снимаем деньги с несуществующего кошелька 
"""
def test_withdraw_not_existable_wallet(client):
    with pytest.raises(Exception):
        
        client.post(f"/api/v1/wallets/{uuid.uuid4()}/operation", 
                            json={"operation_type": "WITHDRAW", "amount": 1000})
        

    
    
