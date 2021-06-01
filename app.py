import MySQLdb
from flask import Flask, jsonify, request
from dotenv import load_dotenv

from db_config import configure_database

load_dotenv()

app = Flask(__name__)

mysql = configure_database(app)


@app.route('/api/students/', methods=['POST', 'GET'])
def students():
    if request.method == 'POST':
        request_data = request.get_json()
        student_id = int(request_data['student_id'])
        student_name = request_data['student_name']
        email = request_data['email']
        phone_number = request_data['phone_number']
        cur = mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO students(student_id, student_name, email, phone_number) "
                        "VALUES (%d, '%s', '%s', '%s')" % (student_id, student_name, email, phone_number))
        except MySQLdb.IntegrityError as err:
            response = {'student_id': student_id, 'status': 'Failure', 'error': str(err)}
        else:
            mysql.connection.commit()
            response = {'student_id': student_id, 'status': 'Success'}
        finally:
            cur.close()
        return jsonify(response)

    elif request.method == 'GET':
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM students")
        response = []
        if result > 0:
            students_table = cur.fetchall()
            for student in students_table:
                response.append({'student_id ': student[0],
                                 'student_name': student[1],
                                 'email': student[2],
                                 'phone_number': student[3]})
        return jsonify({'students': response})


@app.route('/api/students/<int:student_id>/', methods=['GET'])
def get_student_details(student_id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM students WHERE student_id = '%s'" % student_id)
    response = {}
    if result > 0:
        students_table = cur.fetchall()
        for student in students_table:
            response = {'student_id ': student[0],
                        'student_name': student[1],
                        'email': student[2],
                        'phone_number': student[3]}
    else:
        response = {'student_id': student_id, 'error': "Student ID does not exist"}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
