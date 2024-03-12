import sqlite3
class Database:
    
    def __init__(self):
        self.conn = sqlite3.connect('viktorina.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def check_human(self, id):
        self.cursor.execute(f'SELECT chatid FROM user_id WHERE chatid = "{id}"')
        return self.cursor.fetchone()
    
    def all_human(self, id):
        self.cursor.execute(f'SELECT username, name, surname FROM user_id WHERE chatid={id}')
        return self.cursor.fetchone()
    
    def close(self):
        self.conn.close()

    def new_human(self, id, list_names_surnames):
        self.cursor.execute('INSERT INTO user_id VALUES (?, ?, ?, ?, ?);', [id, list_names_surnames[0], 0, list_names_surnames[1], list_names_surnames[2],])
        self.conn.commit()

    def coding(self, id, random_number):
        current_question = {}
        self.cursor.execute(f'SELECT * FROM coding WHERE number = "{random_number}"')
        question = self.cursor.fetchone()
        current_question[id] = {
        'question': question[1],
        'otvet': question[6]
        }
        return [current_question, question]
    
    def score(self, id):
        self.cursor.execute(f'UPDATE user_id SET score = score+10 WHERE chatid={id}')
        self.conn.commit()

    def check_profile(self, id):
        self.cursor.execute(f'SELECT name, surname, score FROM user_id WHERE chatid = {id}')
        return self.cursor.fetchone()

    def physics(self, id, random_number):
        current_question = {}
        self.cursor.execute(f'SELECT * FROM physics WHERE number = "{random_number}"')
        question = self.cursor.fetchone()
        current_question[id] = {
        'question': question[1],
        'otvet': question[6]
        }
        return [current_question, question]
    
    def matem(self, id, random_number):
        current_question = {}
        self.cursor.execute(f'SELECT * FROM matem WHERE number = "{random_number}"')
        question = self.cursor.fetchone()
        current_question[id] = {
        'question': question[1],
        'otvet': question[6]
        }
        return [current_question, question]