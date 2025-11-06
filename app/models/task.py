from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    def to_dict(self) :
        return {
            "id": self.id,
            "title" : self.title,
            "description" : self.description,
            "is_complete" : False if not self.completed_at else True
            #"is_complete" : self.is_complete()
        }
    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title = task_data["title"],
            description = task_data["description"],
            completed_at = task_data.get("completed_at")
        )

    # def is_complete(self):
    #     if self.completed_at is not None:
    #         return True
    #     return False