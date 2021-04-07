import sqlite3


class PersistenceService:


    def __init__(self):
        self.db_file_name = "ml-starter-backend.db"

    def initialize(self):
        con = self.get_db_connection()
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS predictions
                       (id integer primary key,input_data text, prediction text, rating text)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS input_fields
                        (id integer primary key, field_name text, label text, field_type text )''')
        con.commit()
        con.close()
        pass

    def get_db_connection(self):
        return sqlite3.connect(self.db_file_name)

    def save_input_field(self, input_field):
        con = self.get_db_connection()
        cur = con.cursor()


        sql = '''INSERT INTO input_fields (field_name, label, field_type) VALUES (?, ?, ?)'''
        row = (str(input_field['name']), str(input_field['label']), str(input_field['type']))
        cur.execute(sql, row)
        con.commit()
        con.close()

    def save_prediction(self, input_data, prediction):
        con = self.get_db_connection()
        cur = con.cursor()

        sql = '''INSERT INTO predictions (input_data, prediction) VALUES (?, ?)'''
        row = (str(input_data), str(prediction))
        cur.execute(sql, row)

        lastRowId = cur.lastrowid
        con.commit()
        con.close()
        return lastRowId

    def get_all_predictions(self):
        con = self.get_db_connection()
        cur = con.cursor()

        predictions = []
        for row in cur.execute("SELECT * FROM predictions"):
            predictions.append(row)

        con.close()
        return predictions

    def get_input_fields(self):
        con = self.get_db_connection()
        cur = con.cursor()

        input_fields = []
        for row in cur.execute("SELECT * FROM input_fields"):
            input_fields.append(row)

        con.close()
        return input_fields

    def save_rating(self, id, rating):
        con = self.get_db_connection()
        cur = con.cursor()

        sql = '''UPDATE predictions SET rating = ? WHERE id = ?'''
        row = (str(rating), str(id))
        cur.execute(sql, row)
        con.commit()
        con.close()
