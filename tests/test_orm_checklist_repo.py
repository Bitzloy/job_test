from checklists.entities.checklist import CheckList
from checklists.storages.checklist_storage import OrmChecklistRepository
from checklists.commands.checklist import UpdateChecklistCommand, UpdateChecklistRequestDTO


def test_create_orm_checklist_repo(orm_checklist_repo):
    checklist = CheckList.create(title="YAssdsd", description="Checklist")

    orm_checklist_repo.add(checklist)

    expected_checklist = orm_checklist_repo.get_by_id(checklist.uuid)

    assert expected_checklist.title == checklist.title
    assert expected_checklist.description == checklist.description

    orm_checklist_repo.remove(checklist.uuid)


def test_orm_checklist_get_all(orm_checklist_repo, create_orm_checklists):
    checklists = [
        create_orm_checklists(title="я заголовок"),
        create_orm_checklists(title="другой заголовок"),
        create_orm_checklists(title="третий"),
    ]
    all_checklists = orm_checklist_repo.get_all()

    assert all_checklists[0].title == "я заголовок"
    assert all_checklists[1].title == "другой заголовок"
    assert all_checklists[2].title == "третий"
    assert len(all_checklists) == 3


def test_orm_checklist_delete(orm_checklist_repo):
    checklist = CheckList.create(title="YAssdsd", description="Checklist")

    orm_checklist_repo.add(checklist)

    orm_checklist_repo.remove(checklist.uuid)
    all_checklists = orm_checklist_repo.get_all()

    assert all_checklists == []


def test_orm_checklist_update(orm_checklist_repo):
    checklist = CheckList.create(
        title="checklsit", description="Checklistsdsds"
    )
    orm_checklist_repo.add(checklist)


    checklist_to_update = orm_checklist_repo.get_by_id(checklist.uuid)
    checklist_to_update.update(
            title="Я чеклист",
            description="я новый чеклист",
            is_done=True
    )

    
    orm_checklist_repo.update(checklist_to_update)
    expected_result = orm_checklist_repo.get_by_id(checklist_to_update.uuid)

    assert expected_result.title == "Я чеклист"
    assert expected_result.description == "я новый чеклист"
    assert expected_result.is_done == True

    orm_checklist_repo.remove(checklist_to_update.uuid)
