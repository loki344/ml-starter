from abc import ABC, abstractmethod
from typing import List

from persistence.schemas import Prediction


class PersistenceService(ABC):
    """This is the abstract class for any persistence service which
     would like to provide it's services to the REST-API"""

    def __init__(self):
        """Executes a health-check on creation to ensure the functionality"""

        self.health_check()
        pass

    @abstractmethod
    def health_check(self) -> None:
        """
        This method should check the basic functionalities of the extending persistence service.
        You should check connectivity and provide according log or error-messages

        :return: None
        """
        pass

    @abstractmethod
    def save_prediction(self, input_data: str, prediction: str) -> Prediction:
        """
        This method saves the given input_data and prediction in a Prediction object.
        Ensure to set the "created" field and the id in the returned object.

        :param input_data: a string representation of the input
        :type input_data: str

        :param prediction: a string representation fo the prediction

        :type prediction: Prediction

        :return: prediction
        """
        pass

    @abstractmethod
    def save_rating(self, prediction_id: str, rating: str) -> Prediction:
        """
        Updates the Prediction object with the given id and adds the rating.

        :param prediction_id: of the prediction to update
        :type prediction_id: str

        :param rating: string representation of the rating
        :type rating: str

        :return: Prediction
        """
        pass

    @abstractmethod
    def get_predictions(self) -> List[Prediction]:
        """
        Returns all predictions from the datasource.

        :return: List of all predictions
        """
        pass
