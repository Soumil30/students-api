class Students:
    def __init__(self, mysql):
        self.mysql = mysql

    def create_table(self):
        cur = self.mysql.connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS students(student_id INTEGER AUTO_INCREMENT PRIMARY KEY, "
                    "student_name VARCHAR(50), email VARCHAR(50), phone_number VARCHAR(10))")
        cur.execute("ALTER TABLE students AUTO_INCREMENT = 10001")
        self.mysql.connection.commit()
        cur.close()

    def add_new_student(self, request_data):
        student_name = request_data['student_name']
        email = request_data['email']
        phone_number = request_data['phone_number']
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO students(student_name, email, phone_number) VALUES ('%s', '%s', '%s')"
                    % (student_name, email, phone_number))
        self.mysql.connection.commit()
        result = cur.execute("SELECT LAST_INSERT_ID()")
        response = {}
        if result > 0:
            response['student_id'] = str(cur.fetchall()[0][0])
            response['status'] = "Success"
        else:
            response['status'] = "Failed"
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
        cur.close()
        return response

    def get_individual_student(self, student_id):
        cur = self.mysql.connection.cursor()
        result = cur.execute("SELECT * FROM students WHERE student_id = '%s'" % student_id)
        response = {'student_id': student_id}
        if result > 0:
            student_data = cur.fetchall()[0]
            response['student_name'] = student_data[1]
            response['email'] = student_data[2]
            response['phone_number'] = student_data[3]
        else:
            response['error'] = "Student ID does not exist"
        cur.close()
        return response
