import json
from collections import namedtuple

import pymongo
from bson import ObjectId
from pymongo import ReturnDocument

from .persistence_service import PersistenceService


class MongoDbService(PersistenceService):

    def __init__(self, cluster_name: str, db_name: str, db_user: str, db_credentials: str):
        self.clusterName = cluster_name
        self.db_name = db_name
        self.db_user = db_user
        self.db_credentials = db_credentials

        connection_string = "mongodb+srv://"+db_user+":"+db_credentials+"@"+cluster_name+".pnzdz.mongodb.net/"+db_name+"?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(connection_string)

    def save_prediction(self, input_data: str, prediction: str):

        db = self.client[self.db_name]
        prediction_entity = {'input_data': input_data, 'prediction': prediction}
        new_id = str(db.predictions.insert_one(prediction_entity).inserted_id)
        prediction_entity = {"id": new_id, "input_data": input_data, "prediction": prediction}

        return namedtuple("Prediction", prediction_entity.keys())(*prediction_entity.values())

    def save_rating(self, prediction_id, rating):

        db = self.client[self.db_name]
        prediction_entity = db.predictions.find_one_and_update(
            {"_id" : ObjectId(prediction_id)},
            {"$set":
                {"rating": rating}
            }, return_document=ReturnDocument.AFTER)

        prediction = {"id": str(prediction_entity['_id']), "input_data": prediction_entity['input_data'],
                      "prediction": prediction_entity['prediction'], "rating": prediction_entity['rating']}

        return prediction

    def get_predictions(self):
        db = self.client[self.db_name]
        predictions = []
        for prediction in db.predictions.find({}):
            print(type(prediction))
            predictions.append({"id": str(prediction['_id']), "input_data": prediction['input_data'],
                      "prediction": prediction['prediction'], "rating": prediction['rating'] if 'rating' in prediction else ''})

        return predictions
