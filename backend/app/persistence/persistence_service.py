from abc import ABC, abstractmethod
from typing import List

from .schemas import Prediction


class PersistenceService(ABC):

    @abstractmethod
    def save_prediction(self, input_data: str, prediction: str) -> Prediction:
        pass

    @abstractmethod
    def save_rating(self, prediction_id, rating: str) -> Prediction:
        pass

    @abstractmethod
    def get_predictions(self) -> List[Prediction]:
        pass
