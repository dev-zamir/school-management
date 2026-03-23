from fastapi import Query
from dataclasses import dataclass


@dataclass
class PaginationParams:
    """
    Reusable pagination dependency.
    Usage: pagination: PaginationParams = Depends()
    """
    page: int = Query(default=1, ge=1, description="Page number")
    per_page: int = Query(default=20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        return self.per_page
