from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PredictionBase(BaseModel):
    """Base representation of a prediction"""
    input_data: str
    created: datetime
    prediction: str


class Prediction(PredictionBase):
    """Prediction which is used after the creation in the datasource"""

    id: str
    rating: Optional[str]

    class Config:
        orm_mode = True


class PredictionCreate(PredictionBase):
    """Prediction which is used to initially create a prediction in the datasource"""
    pass


class PredictionPatch(BaseModel):
    """Prediction which is used to update the rating in a prediction"""
    id: str
    rating: str


