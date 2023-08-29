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

    def insert_questions(self, questions: list[dict]):
        insertion_values = [f"('''{question['question']}''', '''{question['answer']}''')\n\n" for question in questions]
        with open('l0.txt', 'w+', encoding='utf-8') as file:
            file.write(', '.join(insertion_values))
        insertion = f'''
        INSERT INTO 'Questions' ('question', 'answer')  VALUES {', '.join(insertion_values)}
        '''
        self.cursor.execute(insertion)
        self.connection.commit()

    def get_question(self, question_id: int):
        self.cursor.execute(f'''
        SELECT * FROM 'Questions' WHERE id={question_id}
        ''')
        question = self.cursor.fetchall()[0]
        return question


if __name__ == '__main__':
    from quiz_questions import get_random_question
    q = [get_random_question() for x in range(5)]
    db = QuestionsDatabase()
    with db:

        print(db.get_question(1))
