import mysql.connector


class Database:
    def __init__(self, host, port, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
        )
        self.cursor = self.connection.cursor()

        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        self.connection.commit()

        self.cursor.execute(f"USE {database}")
        self.connection.commit()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL
            )
        """)
        self.connection.commit()

    def close_connection(self):
        self.connection.close()

    def get_students(self):
        query = "SELECT * FROM students"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return [{'id': row[0], 'name': row[1], 'age': row[2]} for row in result]

    def get_student_by_id(self, student_id):
        query = "SELECT * FROM students WHERE id = %s"
        self.cursor.execute(query, (student_id,))
        result = self.cursor.fetchone()
        return {'id': result[0], 'name': result[1], 'age': result[2]} if result else None

    def create_student(self, name, age):
        query = "INSERT INTO students (name, age) VALUES (%s, %s)"
        self.cursor.execute(query, (name, age))
        self.connection.commit()
        return {'id': self.cursor.lastrowid, 'name': name, 'age': age}

    def update_student(self, student_id, name, age):
        query = "UPDATE students SET name = %s, age = %s WHERE id = %s"
        self.cursor.execute(query, (name, age, student_id))
        self.connection.commit()
        return {'id': student_id, 'name': name, 'age': age}

    def delete_student(self, student_id):
        query = "DELETE FROM students WHERE id = %s"
        self.cursor.execute(query, (student_id,))
        self.connection.commit()
        return True
