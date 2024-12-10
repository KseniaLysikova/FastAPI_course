from datetime import datetime
from sqlalchemy import ForeignKey, BigInteger, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from models.user import Base


class Project(Base):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    help_information: Mapped[str] = mapped_column(nullable=False)
    bot_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    default_attendant_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                 server_default=func.current_timestamp())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                 server_default=func.current_timestamp())


class ProjectUsers(Base):
    __tablename__ = 'project_users'

    project_id: Mapped[int] = mapped_column(ForeignKey('project.id', ondelete="CASCADE"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"), primary_key=True)
    is_on_duty: Mapped[bool] = mapped_column(nullable=False)


class DutySchedule(Base):
    __tablename__ = 'duty_schedule'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('project.id', ondelete="CASCADE"), nullable=False)
    attendant_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    from_date: Mapped[datetime] = mapped_column(nullable=False)
    to_date: Mapped[datetime] = mapped_column(nullable=False)
