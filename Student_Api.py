from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from database import Database

app = Flask(__name__)
db = Database('localhost', '3306', 'root', 'Apple.nextiva@123', 'db_student')
 
auth=HTTPBasicAuth()
USERDATA ={
     "admin":"shruti@123"
 }

@auth.verify_password
def verify_password(username,password):
    if username in USERDATA and USERDATA[username]==password:
        return username
    return None

@app.route('/students', methods=['GET'])
@auth.login_required
def get_students():
    students = db.get_students()
    return jsonify({'students': students})


@app.route('/students/<int:student_id>', methods=['GET'])
@auth.login_required
def get_student(student_id):
    student = db.get_student_by_id(student_id)
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({'student': student})


@app.route('/students', methods=['POST'])
@auth.login_required
def create_student():
    data = request.get_json()

    if 'name' not in data or 'age' not in data:
        return jsonify({'error': 'Name and age are required'}), 400

    name = data['name']
    age = data['age']
    new_student = db.create_student(name, age)

    return jsonify({'student': new_student}), 201


@app.route('/students/<int:student_id>', methods=['PUT'])
@auth.login_required
def update_student(student_id):
    student = db.get_student_by_id(student_id)
    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    data = request.get_json()
    name = data.get('name', student['name'])
    age = data.get('age', student['age'])
    updated_student = db.update_student(student_id, name, age)

    return jsonify({'student': updated_student})


@app.route('/students/<int:student_id>', methods=['DELETE'])
@auth.login_required
def delete_student(student_id):
    student = db.get_student_by_id(student_id)
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    else:
        db.delete_student(student_id)
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
