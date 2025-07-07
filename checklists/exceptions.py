class ApiError(Exception):
    message = None
    status_code = None
    details = None


class CheckListNotFoundApiError(ApiError):
    status_code = 404
    message = "CHECKLIST_NOT_FOUND"
    details = {
        "status_code": status_code,
        "field": "uuid",
        "what_happened": "Чеклист с таким uuid не найден/не существует",
    }


class ChecklistValidationApiError(ApiError):
    status_code = 400
    message = "CHECKLIST_VALIDATION"
    details = {
        "status_code": status_code,
        "field": "title",
        "what_happened": "Недопустимое значение поля title",
    }


class ChecklistIsExistApiError(ApiError):
    status_code = 409
    message = "CHECKLIST_IS_EXIST!"
    details = {
        "status_code": status_code,
        "field": "uuid",
        "what_happened": "Чеклист с таким uuid уже существует",
    }


class ItemNotFoundApiError(ApiError):
    status_code = 404
    message = "ITEM_NOT_FOUND"
    details = {
        "status_code": status_code,
        "field": "id",
        "what_happened": "Айтем с таким id не найден/не существует",
    }



class ValidationApiError(ApiError):
    def __init__(self, message: str):
        self.message = message
        
    status_code = 400