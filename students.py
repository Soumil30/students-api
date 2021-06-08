import MySQLdb


class Students:
    def __init__(self, mysql):
        self.mysql = mysql

    def add_new_student(self, request_data):
        student_id = int(request_data['student_id'])
        student_name = request_data['student_name']
        email = request_data['email']
        phone_number = request_data['phone_number']
        cur = self.mysql.connection.cursor()
        try:
            cur.execute("INSERT INTO students(student_id, student_name, email, phone_number) "
                        "VALUES (%d, '%s', '%s', '%s')" % (student_id, student_name, email, phone_number))
        except MySQLdb.IntegrityError as err:
            response = {'student_id': student_id, 'status': 'Failure', 'error': str(err)}
        else:
            self.mysql.connection.commit()
            response = {'student_id': student_id, 'status': 'Success'}
        finally:
            cur.close()
        return response

    def get_all_students(self):
        cur = self.mysql.connection.cursor()
        result = cur.execute("SELECT * FROM students")
        response = []
        if result > 0:
            students_table = cur.fetchall()
            for student in students_table:
                response.append({'student_id ': student[0],
                                 'student_name': student[1],
                                 'email': student[2],
                                 'phone_number': student[3]})
        return response

    def get_individual_student(self, student_id):
        cur = self.mysql.connection.cursor()
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
        return response
