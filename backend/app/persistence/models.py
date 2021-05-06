from sqlalchemy import Column, Integer, String, DateTime
from persistence.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime)
    input_data = Column(String)
    prediction = Column(String)
    rating = Column(String)

