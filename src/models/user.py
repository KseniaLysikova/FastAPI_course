from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    __password: Mapped[str] = mapped_column("password", nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    telegram_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    is_supervisor: Mapped[bool] = mapped_column(nullable=False, default=False)

    user_info = relationship('UserInfo', back_populates='User')
    projects = relationship('ProjectUsers', back_populates='User')

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
    __tablename__ = 'UserInfo'

    user_id: Mapped[str] = mapped_column(ForeignKey('User.id'), primary_key=True)
    surname: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    patronymic: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=False, unique=True)
    position: Mapped[str] = mapped_column(nullable=False)
    telegram_token: Mapped[str] = mapped_column(nullable=False, unique=True)

    user = relationship('User', back_populates='UserInfo')
