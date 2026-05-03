from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date

Base = declarative_base()
engine = create_engine("sqlite:///data/finance.db")
Session = sessionmaker(bind=engine)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    amount = Column(Float)
    type = Column(String)
    category = Column(String)
    note = Column(String)
    date = Column(Date, default=date.today)


def init_db():
    Base.metadata.create_all(engine)


def add_transaction(user_id, amount, type_, category, note, date_=None):
    session = Session()
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
    session = Session()
    results = session.query(Transaction).filter_by(user_id=user_id).all()
    session.close()
    return results