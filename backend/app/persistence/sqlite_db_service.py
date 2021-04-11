from fastapi_sqlalchemy import DBSessionMiddleware, db

from . import models
from .database import engine, SQLALCHEMY_DATABASE_URL
from .persistence_service import PersistenceService


class InMemoryDbService(PersistenceService):

    def __init__(self, app):
        models.Base.metadata.create_all(bind=engine)
        app.add_middleware(DBSessionMiddleware,
                           db_url=SQLALCHEMY_DATABASE_URL)

    def save_prediction(self, input_data: str, prediction: str):

        prediction_entity = models.Prediction(input_data=str(input_data), prediction=str(prediction))
        db.session.add(prediction_entity)
        db.session.commit()
        db.session.refresh(prediction_entity)

        return prediction_entity

    def save_rating(self, prediction_id, rating):
        existing_prediction = db.session.query(models.Prediction).get(prediction_id)
        existing_prediction.rating = rating
        db.session.commit()
        db.session.refresh(existing_prediction)

        return existing_prediction

    def get_predictions(self):
        return db.session.query(models.Prediction).all()
