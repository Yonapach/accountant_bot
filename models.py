from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr, relationship


class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class User(Base):
    username = Column(String(150), unique=True, nullable=False)
    first_name = Column(String(100))
    debts = relationship("Debt", back_populates="user")

    def debt_sum(self, chat_id: int) -> float:
        return sum([debt.amount for debt in self.debts if debt.chat_id == chat_id])


class Debt(Base):
    amount = Column(Float, nullable=False)
    chat_id = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship(User, back_populates="debts")
