from enum import StrEnum


class EnumRequestStatus(StrEnum):
    created = "created"
    in_work = "in_work"
    completed = "completed"
    closed = "closed"


class EnumOrderByType(StrEnum):
    ascending = "ascending"
    descending = "descending"