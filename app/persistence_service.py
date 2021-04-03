import sqlite3


class PersistenceService:


    def __init__(self):
        self.db_file_name = "ml-starter-backend.db"

    def initialize(self):
        con = self.get_db_connection()
        cur = con.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS predictions
                       (id integer primary key,input_data text, prediction text )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS input_fields
                        (id integer primary key, field_name text, description text, field_type text )''')
        con.commit()
        con.close()
        pass

    def get_db_connection(self):
        return sqlite3.connect(self.db_file_name)

    def save_input_field(self, input_field):
        con = self.get_db_connection()
        cur = con.cursor()

        print(input_field)
        sql = '''INSERT INTO input_fields (field_name, description, field_type) VALUES (?, ?, ?)'''
        row = (str(input_field['name']), str(input_field['description']), str(input_field['type']))
        cur.execute(sql, row)
        con.commit()
        con.close()

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

    def get_input_fields(self):
        con = self.get_db_connection()
        cur = con.cursor()

        input_fields = []
        for row in cur.execute("SELECT * FROM input_fields"):
            input_fields.append(row)

        con.close()
        return input_fields
