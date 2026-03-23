from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, resource: str, id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} with id '{id}' not found",
        )


class AlreadyExistsError(HTTPException):
    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} with {field} '{value}' already exists",
        )


class ForbiddenError(HTTPException):
    def __init__(self, message: str = "You don't have permission to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
        )


class BusinessRuleError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message,
        )


# Domain-specific exceptions (add more as you build phases)
class StudentNotFoundError(NotFoundError):
    def __init__(self, student_id: str):
        super().__init__("Student", student_id)


class ClassFullError(BusinessRuleError):
    def __init__(self):
        super().__init__("This class has reached its maximum capacity")


class DuplicateEnrollmentError(BusinessRuleError):
    def __init__(self):
        super().__init__("Student is already enrolled in this class")
