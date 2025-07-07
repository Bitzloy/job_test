import pytest

# from recursive_diff import recursive_eq
# from pytest_mock import MockerFixture
import pprint
from flask import jsonify
import uuid


from checklists.storages.checklist_storage import (
    SqliteChecklistRepository,
    AbstractChecklistsRepository,
)
from checklists.entities.checklist import CheckList
from checklists.exceptions import ChecklistIsExistApiError


def test_post_request(client, checklist_repository: SqliteChecklistRepository):
    response = client.post(
        "/api/checklists/",
        json={"title": "Checklist", "description": "Это чеклист"},
    )
    json_response = response.json
    # print(json_response)

    assert json_response["title"] == "Checklist"
    assert json_response["description"] == "Это чеклист"
    assert json_response["uuid"] == str(uuid.UUID(json_response["uuid"]))
    assert "created_at", "updated_at" in json_response
    assert response.status_code == 200

    checklist_repository.remove(json_response["uuid"])


def test_get_all_request(client, create_checklist):
    checklists = [
        create_checklist(title="я заголовок"),
        create_checklist(title="другой заголовок"),
        create_checklist(title="третий"),
    ]
    response = client.get("/api/checklists/")
    json_response = response.json

    assert json_response[0]["title"] == checklists[0].title
    assert json_response[1]["title"] == checklists[1].title
    assert json_response[0]["description"] == "Это чеклист"
    assert json_response[0]["uuid"] == str(uuid.UUID(json_response[0]["uuid"]))
    assert "created_at", "updated_at" in json_response[0]
    assert response.status_code == 200
    assert len(json_response) == 3


def test_get_by_id(
    client, create_checklist, checklist_repository
):  # с помощью фикстуры создания чеклиста
    checklist = create_checklist(title="заголовок ", description="описание")

    response = client.get(f"/api/checklists/{checklist.uuid}")
    json_response = response.json

    assert json_response["uuid"] == checklist.uuid
    assert response.status_code == 200


def test_put_request(client, create_checklist):
    checklist = create_checklist(
        title="Я чеклист", description="Это новый чеклист"
    )

    client.put(
        f"/api/checklists/{checklist.uuid}",
        json={"title": "Я чеклист", "description": "Это новый чеклист"},
    )

    response = client.get(f"/api/checklists/{checklist.uuid}")
    json_response = response.json

    assert json_response["title"] == "Я чеклист"
    assert json_response["description"] == "Это новый чеклист"
    assert response.status_code == 200


def test_delete_request(client):
    request_1 = client.post(
        "/api/checklists/",
        json={"title": "Checklist", "description": "Это чеклист"},
    )
    json_request_1 = request_1.json

    client.delete(f'/api/checklists/{json_request_1["uuid"]}')

    response = client.get(f"/api/checklists/")
    json_response = response.json

    assert json_response == []
    assert response.status_code == 200


# def test_CheckListNotFoundApiError(client):
#     response = client.get(f'/api/checklists/{uuid.uuid4()}')


#     assert response.json == {
#        'code': 'CHECKLIST_NOT_FOUND',
#        'details': {
#            'field': 'id',
#            'status_code': 404,
#            'what_happened': 'Чеклист с таким id не найден/не существует',
#        },
#     }
#     assert response.status_code == 404


# def test_change_ChecklistValidationApiError(client, create_checklist):
#     checklist = create_checklist(title="Я чеклист", description="Это новый чеклист")

#     response = client.put(f'/api/checklists/{checklist.uuid}',
#         json={
#             "title": "Г",
#             "description": "неудачное название"
#         })


#     assert response.json == {
#        'code': 'CHECKLIST_VALIDATION',
#        'details': {
#            'field': 'title',
#            'status_code': 400,
#            'what_happened': 'Недопустимое значение поля title',
#        },
#    }
#     assert response.status_code == 400


# def test_create_ChecklistValidationApiError(client):
#     response = client.post("/api/checklists/",
#         json={
#             "title": "Chsdksdjajdajdsdksjdksjdksjdksdjskjdkskdjksjdsjdksjkdjskdjksjdjkjsdkjsjdkjsdjksdjksjd",
#             "description": "Это чеклист"
#         } )


#     assert response.json == {
#        'code': 'CHECKLIST_VALIDATION',
#        'details': {
#            'field': 'title',
#            'status_code': 400,
#            'what_happened': 'Недопустимое значение поля title',
#        },
#    }
#     assert response.status_code == 400


# def test_Internal_error(client):
#     response = client.post("/api/checklists/",
#         json={
#             "titlese": "Я заголовок",
#             "description": "Это чеклист"
#         } )


#     assert response.json == {
#                         "code": "INTERNAl",
#                         "details": "Ошибка кода"
#                         }

#     assert response.status_code == 500


# def test_ChecklistIsExistApiError(checklist_repository: SqliteChecklistRepository, create_checklist):
#     checklist = create_checklist(title="title", description="description")
#     with pytest.raises(ChecklistIsExistApiError):
#         checklist_repository.add(checklist=checklist)


# def test_database_error(client):
#     response = client.post("/api/checklists/",
#         json={
#             "title": "Я заголовок",
#             "description": "Это чеклист"
#         } )


#     assert response.json == {
#                         "code": "SQLITE_ERROR",
#                         "details": "Ошибка запроса"
#                         }

#     assert response.status_code == 400
