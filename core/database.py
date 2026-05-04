from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date
import os

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    amount = Column(Float)
    type = Column(String)
    category = Column(String)
    note = Column(String)
    date = Column(Date, default=date.today)

def get_session(user_id):
    os.makedirs("data", exist_ok=True)
    engine = create_engine(f"sqlite:///data/{user_id}.db")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

def init_db():
    pass


def add_transaction(user_id, amount, type_, category, note, date_=None):
    session = get_session(user_id)
    t = Transaction(
        user_id=user_id,
        amount=amount,
        type=type_,
        category=category,
        note=note,
        date=date_ or date.today()
    )
    session.add(t)
    session.commit()
    session.close()


def get_transactions(user_id):
    session = get_session(user_id)
    results = session.query(Transaction).all()
    session.close()
    return results