import sqlite3


class PersistenceService:


    def __init__(self):
        self.db_file_name = "ml-starter-backend.db"

    def initialize(self):
        con = self.get_db_connection()
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS predictions
                       (id integer primary key,input_data text, prediction text )''')
        con.commit()
        con.close()
        pass

    def get_db_connection(self):
        return sqlite3.connect(self.db_file_name)

    def save_prediction(self, input_data, prediction):
        con = self.get_db_connection()
        cur = con.cursor()

        sql = '''INSERT INTO predictions (input_data, prediction) VALUES (?, ?)'''
        row = (str(input_data), str(prediction))
        cur.execute(sql, row)
        con.commit()
        con.close()

    def get_all_predictions(self):
        con = self.get_db_connection()
        cur = con.cursor()

        predictions = []
        for row in cur.execute("SELECT * FROM predictions"):
            predictions.append(row)

        con.close()
        return predictions
