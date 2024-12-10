from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    __password: Mapped[str] = mapped_column("password", nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    telegram_id: Mapped[str] = mapped_column(nullable=True, unique=True)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    is_supervisor: Mapped[bool] = mapped_column(nullable=False, default=False)

    @hybrid_property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = pwd_context.hash(password)

    @hybrid_method
    def verify_password(self, password):
        return pwd_context.verify(password, self.__password)


class UserInfo(Base):
    __tablename__ = 'user_info'

    user_id: Mapped[str] = mapped_column(ForeignKey('user.id', ondelete="CASCADE"), primary_key=True)
    surname: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True, unique=True)
    position: Mapped[str] = mapped_column(nullable=True)
    telegram_token: Mapped[str] = mapped_column(BigInteger, nullable=True, unique=True)
