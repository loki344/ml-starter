import datetime
from typing import List

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from persistence import models
from persistence.database import engine, SQLALCHEMY_DATABASE_URL
from persistence.models import Prediction
from persistence.persistence_service import PersistenceService


class InMemoryDbService(PersistenceService):
    """This service handles the persistence in a in memory SQLite database.
    It is located in the persistence directory"""

    def __init__(self, app: FastAPI):
        """
        Initializes the datasource for the ven FastAPI application

        :param app: FastAPI application where this service is used
        :type app: FastAPI
        """

        models.Base.metadata.create_all(bind=engine)
        app.add_middleware(DBSessionMiddleware,
                           db_url=SQLALCHEMY_DATABASE_URL)
        super().__init__()

    def health_check(self) -> None:
        print("Verifiying connection to the SQLite InMemory database")
        with db():
            print(db.session.is_active)
        print("Connection test successful")
        print("-------------------------------------------------------------------------------------------------------")

        pass

    def save_prediction(self, input_data: str, prediction: str) -> Prediction:
        prediction_entity = models.Prediction(input_data=str(input_data), prediction=str(prediction),
                                              created=datetime.datetime.now())
        db.session.add(prediction_entity)
        db.session.commit()
        db.session.refresh(prediction_entity)

        return prediction_entity

    def save_rating(self, prediction_id: str, rating: str) -> Prediction:
        existing_prediction = db.session.query(models.Prediction).get(prediction_id)
        existing_prediction.rating = rating
        db.session.commit()
        db.session.refresh(existing_prediction)

        return existing_prediction

    def get_predictions(self) -> List[Prediction]:
        return db.session.query(models.Prediction).all()
