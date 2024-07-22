from datetime import datetime
from sqlalchemy import ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from models.user import Base

RequestStatus = ENUM(
    'created', 'in_work', 'completed', 'closed',
    name='request_status', metadata=Base.metadata
)

RequestType = ENUM(
    'telegram',
    name='request_type', metadate=Base.metadata
)


class Request(Base):
    __tablename__ = 'Request'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('Project.id'))
    requester_name: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    request_type: Mapped[RequestType] = mapped_column(RequestType, nullable=False)
    status: Mapped[RequestStatus] = mapped_column(RequestStatus, nullable=False)
    attendant_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                 server_default=func.current_timestamp())
    finished_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                  server_default=func.current_timestamp())

    user = relationship('User', back_populates='Request')
    project = relationship('Project', back_populates='Request')
    telegram_request = relationship('TelegramRequest', back_populates='Request')


class TelegramRequest(Base):
    __tablename__ = 'TelegramRequest'

    id: Mapped[int] = mapped_column(ForeignKey('Request.id'), primary_key=True)
    telegram_id: Mapped[int] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)

    request = relationship('Request', back_populates='TelegramRequest')
