from typing import Optional

from pydantic import BaseModel


class PredictionBase(BaseModel):
    input_data: str
    prediction: str


class Prediction(PredictionBase):

    id: int
    rating: Optional = str

    class Config:
        orm_mode = True


class PredictionCreate(PredictionBase):
    pass


class PredictionPatch(BaseModel):
    id: str
    rating: str


