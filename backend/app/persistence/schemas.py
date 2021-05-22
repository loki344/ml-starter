import ast
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PredictionBase(BaseModel):
    """Base representation of a prediction"""
    input_data: str


class Prediction(PredictionBase):
    """Prediction which is used after the creation in the datasource"""

    id: str
    rating: Optional[str]
    created: datetime
    prediction: str

    def __repr__(self):

        try:
            formatted_prediction = ast.literal_eval(self.prediction)
        except ValueError:
            formatted_prediction = self.prediction

        return {"id": self.id, "created": self.created,
                     "input_data": self.input_data, "prediction": formatted_prediction,
                     "rating": self.rating}


    class Config:
        orm_mode = True


class PredictionCreate(PredictionBase):
    """Prediction which is used to initially create a prediction in the datasource"""
    pass


class PredictionPatch(BaseModel):
    """Prediction which is used to update the rating in a prediction"""
    rating: str
