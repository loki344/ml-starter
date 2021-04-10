from sqlalchemy import Column, Integer, String
from .database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    input_data = Column(String)
    prediction = Column(String)
    rating = Column(String)

