import ast

from sqlalchemy import Column, Integer, String, DateTime

from persistence.database import Base


class Prediction(Base):
    """This model is primarily used by SQLite. It's corresponding representation for the REST-API is in schemas.py"""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime)
    input_data = Column(String)
    prediction = Column(String)
    rating = Column(String)

    def __repr__(self):

        try:
            formatted_prediction = ast.literal_eval(self.prediction)
        except ValueError:
            formatted_prediction = self.prediction

        return {"id": self.id, "created": self.created,
                     "input_data": self.input_data, "prediction": formatted_prediction,
                     "rating": self.rating}
