import pytest
import uuid
from dataclasses import asdict

from checklists.storages.checklist_storage import OrmChecklistRepository
from checklists.exceptions import ChecklistIsExistApiError
from checklists.commands.checklist import CreateChecklistCommand
from checklists.entities.checklist import CheckList


def test_CheckListNotFoundApiError(client):
    response = client.get(f"/api/checklists/{uuid.uuid4()}")

    assert response.json == {
        "code": "CHECKLIST_NOT_FOUND",
        "details": {
            "field": "uuid",
            "status_code": 404,
            "what_happened": "Чеклист с таким uuid не найден/не существует",
        },
    }
    assert response.status_code == 404


def test_change_ChecklistValidationApiError(client, create_orm_checklists):
    checklist = create_orm_checklists(
        title="Я чеклист", description="Это новый чеклист"
    )

    response = client.put(
        f"/api/checklists/{checklist[0].uuid}",
        json={"title": "Г", "description": "неудачное название", "is_done": False},
    )

    assert response.json == {
        "code": "CHECKLIST_VALIDATION",
        "details": {
            "field": "title",
            "status_code": 400,
            "what_happened": "Недопустимое значение поля title",
        },
    }
    assert response.status_code == 400


def test_create_ChecklistValidationApiError(client):
    response = client.post(
        "/api/checklists/",
        json={
            "title": "Chsdksdjajdajdsdksjdksjdksjdksdjskjdkskdjksjdsjdksjkdjskdjksjdjkjsdkjsjdkjsdjksdjksjd",
            "description": "Это чеклист",
        },
    )

    assert response.json == {
        "code": "CHECKLIST_VALIDATION",
        "details": {
            "field": "title",
            "status_code": 400,
            "what_happened": "Недопустимое значение поля title",
        },
    }
    assert response.status_code == 400


def test_Internal_error(client):
    response = client.post(
        "/api/checklists/",
        json={"titlese": "Я заголовок", "description": "Это чеклист"},
    )

    assert response.json == {"code": "INTERNAl", "details": "Ошибка кода"}

    assert response.status_code == 500


