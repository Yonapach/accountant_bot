from db import Session
from models import User, Debt


def get_or_create_user(session: Session, username: str) -> User:
    user = session.query(User).filter_by(username=username).first()

    if not user:
        user = User(username=username)
        session.add(user)
        session.flush()

    return user


def add_debt(session: Session, user: User, amount: float, chat_id: int) -> None:
    session.add(Debt(amount=amount, user=user, chat_id=chat_id))
    session.flush()


def get_message(debt_sum: float) -> str:
    debt_sum = int(debt_sum)

    if debt_sum > 0:
        msg = f"Тебе должны {debt_sum}"
    elif debt_sum < 0:
        msg = f"Ты должен {-debt_sum}"
    else:
        msg = "Все четко"

    return msg
