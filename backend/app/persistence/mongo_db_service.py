import datetime
from collections import namedtuple
from typing import List

import pymongo
from bson import ObjectId
from pymongo import ReturnDocument

from persistence.persistence_service import PersistenceService
from persistence.schemas import Prediction


class MongoDbService(PersistenceService):
    """This class handles the connection to a MongoDB on https://www.mongodb.com/. Currently no other
    hosting provider has been tested."""

    def __init__(self, cluster_name: str, db_name: str, db_user: str, db_credentials: str):
        """
        Initializes the service with the necessary parameters.

        :param cluster_name: name of the cluster on https://www.mongodb.com/
        :type cluster_name: str

        :param db_name: name of the database
        :type db_name: str

        :param db_user: name of the configured user
        :type db_user: str

        :param db_credentials: for the db_user
        :type db_credentials: str
        """

        self.clusterName = cluster_name
        self.db_name = db_name
        self.db_user = db_user
        self.db_credentials = db_credentials

        connection_string = "mongodb+srv://" + db_user + ":" + db_credentials + "@" + cluster_name + ".pnzdz.mongodb.net/" + db_name + "?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(connection_string)
        super().__init__()

    def health_check(self) -> None:
        print("Verifiying connection to the MongoDB with dbName: " + self.db_name + " ,dbUser: " + self.db_user +
              ", clusterName: " + self.clusterName)
        print(self.client.server_info())
        print("Connection test successful")
        print("-------------------------------------------------------------------------------------------------------")
        pass

    def save_prediction(self, input_data: str, prediction: str) -> Prediction:
        db = self.client[self.db_name]
        created_time = datetime.datetime.now()
        prediction_entity = {'input_data': input_data, 'created': created_time, 'prediction': prediction}
        new_id = str(db.predictions.insert_one(prediction_entity).inserted_id)
        prediction_entity = {"id": new_id, "input_data": input_data, 'created': created_time, "prediction": prediction}

        return namedtuple("Prediction", prediction_entity.keys())(*prediction_entity.values())

    def save_rating(self, prediction_id: str, rating: str) -> Prediction:
        db = self.client[self.db_name]
        prediction_entity = db.predictions.find_one_and_update(
            {"_id": ObjectId(prediction_id)},
            {"$set":
                 {"rating": rating}
             }, return_document=ReturnDocument.AFTER)

        prediction = {"id": str(prediction_entity['_id']), "created": prediction_entity['created'],
                      "input_data": prediction_entity['input_data'],
                      "prediction": prediction_entity['prediction'], "rating": prediction_entity['rating']}

        return namedtuple("Prediction", prediction.keys())(*prediction.values())

    def get_predictions(self) -> List[Prediction]:
        db = self.client[self.db_name]
        predictions = []
        for prediction in db.predictions.find({}):
            prediction_object = {"id": str(prediction['_id']), "input_data": prediction['input_data'],
                                 "created": prediction['created'],
                                 "prediction": prediction['prediction'],
                                 "rating": prediction['rating'] if 'rating' in prediction else None}

            predictions.append(namedtuple("Prediction", prediction_object.keys())(*prediction_object.values()))

        return predictions
