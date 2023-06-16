from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, Integer, String, Time
from sqlalchemy_utils.types import ChoiceType

from src.database import Base


class Audience(Base):
    __tablename__ = "audience"

    DAY_OF_WEEK = (
        ("ПОНЕДЕЛЬНИК", "Понедельник"),
        ("ВТОРНИК", "Вторник"),
        ("СРЕДА", "Среда"),
        ("ЧЕТВЕРГ", "Четверг"),
        ("ПЯТНИЦА", "Пятница"),
        ("СУББОТА", "Суббота"),
    )

    PARITY = (
        ("чёт", "Чётная"),
        ("нечёт", "Нечётная")
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    audience: Mapped[str] = mapped_column(
        String(length=10), nullable=True
    )
    event: Mapped[str] = mapped_column(
        String, nullable=False
    )
    day_of_week = Column(ChoiceType(choices=DAY_OF_WEEK))
    parity = Column(ChoiceType(choices=PARITY))
    start_of_class = Column(Time)
    end_of_class = Column(Time)

    def __repr__(self):
        return f"<Audience {self.id}>"
