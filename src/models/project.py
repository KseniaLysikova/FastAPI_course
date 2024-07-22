from sqlalchemy import ForeignKey, DateTime, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from user import Base


class Project(Base):
    __tablename__ = 'Project'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    help_information: Mapped[str] = mapped_column(nullable=False)
    bot_id: Mapped[int] = mapped_column(nullable=False)
    default_attendant_id: Mapped[int] = mapped_column(ForeignKey('Users.id'), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                 server_default=func.current_timestamp())
    updated_at: Mapped[DateTime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                 server_default=func.current_timestamp())

    default_attendant = relationship('User', back_populates='Project')
    users = relationship('ProjectUsers', back_populates='Project')
    duty_schedule = relationship('DutySchedule', back_populates='Project')
    request = relationship('Request', back_populates='Project')


class ProjectUsers(Base):
    __tablename__ = 'ProjectUsers'

    project_id: Mapped[int] = mapped_column(ForeignKey('Project.id'), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'), primary_key=True)
    is_on_duty: Mapped[bool] = mapped_column(nullable=False)

    user = relationship('User', back_populates='ProjectUser')
    project = relationship('Project', back_populates='ProjectUser')


class DutySchedule(Base):
    __tablename__ = 'DutySchedule'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('Project.id'), nullable=False)
    attendant_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)
    from_date: Mapped[DateTime] = mapped_column(nullable=False)
    to_date: Mapped[DateTime] = mapped_column(nullable=False)

    user = relationship('User', back_populates='DutySchedule')
    project = relationship('Project', back_populates='DutySchedule')
