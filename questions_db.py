import sqlite3


class QuestionsDatabase:
    """Class for questions storing. Use only as a context manager.

    Example:
        # >>> db = QuestionsDatabase()
        # >>> with db:
        # >>>     db.create_questions_table()
    """

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def __init__(self, db_name: str = 'db.sqlite3'):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_questions_table()
        self.connection.close()

    def _create_questions_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Questions (
            id INTEGER PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def insert_question(self, question: dict):
        insertion_value = f"('{question['question']}', '{question['answer']}')"
        insertion = f'''
        INSERT INTO 'Questions' ('question', 'answer')  VALUES {insertion_value}
        '''
        self.cursor.execute(insertion)
        self.connection.commit()

    def get_question(self, question_id: int):
        self.cursor.execute(f'''
        SELECT * FROM 'Questions' WHERE id={question_id}
        ''')
        question = self.cursor.fetchall()[0]
        return question
