from datetime import datetime
from sqlalchemy import ForeignKey, BigInteger, TIMESTAMP, func
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
    __tablename__ = 'request'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('project.id', ondelete="CASCADE"))
    requester_name: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    request_type: Mapped[RequestType] = mapped_column(RequestType, nullable=False)
    status: Mapped[RequestStatus] = mapped_column(RequestStatus, nullable=False)
    attendant_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                 server_default=func.current_timestamp())
    finished_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                  server_default=func.current_timestamp())


class TelegramRequest(Base):
    __tablename__ = 'telegram_request'

    id: Mapped[int] = mapped_column(ForeignKey('request.id', ondelete="CASCADE"), primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(nullable=False)
