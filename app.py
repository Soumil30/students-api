from flask import Flask, jsonify, request
from dotenv import load_dotenv

from db_config import configure_database
from students import Students

load_dotenv()

app = Flask(__name__)

mysql = configure_database(app)

student_db = Students(mysql)


@app.route('/api/students/', methods=['POST', 'GET'])
def students():
    if request.method == 'POST':
        request_data = request.get_json()
        response = student_db.add_new_student(request_data)
        return jsonify(response)

    elif request.method == 'GET':
        response = student_db.get_all_students()
        return jsonify({'students': response})


@app.route('/api/students/<int:student_id>/', methods=['GET'])
def get_student_details(student_id):
    response = student_db.get_individual_student(student_id)
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
