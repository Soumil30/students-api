import MySQLdb
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['JSON_SORT_KEYS'] = False

mysql = MySQL(app)


@app.route('/api/students/', methods=['POST', 'GET'])
def students():
    if request.method == 'POST':
        request_data = request.form
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