import sqlite3
class Database:
    
    def __init__(self):
        self.conn = sqlite3.connect('viktorina.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def check_human(self, id):
        self.cursor.execute(f'SELECT chatid FROM viktorina WHERE chatid = "{id}"')
        return self.cursor.fetchone()
    
    def all_human(self, id):
        self.cursor.execute(f'SELECT username, name, surname FROM viktorina WHERE chatid={id}')
        return self.cursor.fetchone()
    
    def close(self):
        self.conn.close()

    def new_human(self, id, list_names_surnames):
        self.cursor.execute('INSERT INTO viktorina VALUES (?, ?, ?, ?, ?);', [id, list_names_surnames[0], 0, list_names_surnames[1], list_names_surnames[2],])
        self.conn.commit()

    def programming(self, chat_id):
        current_question = {}
        self.cursor.execute('SELECT * FROM coding ORDER BY RANDOM() LIMIT 1')
        question = self.cursor.fetchone()
        current_question[chat_id] = {
        'question': question[1],
        'otvet': question[6],
        'number': question[0]
        }
        return [current_question, question]
    
    def score(self, id):
        self.cursor.execute(f'UPDATE viktorina SET score = score+10 WHERE chatid={id}')
        self.conn.commit()
