from App.database import db
from App.models import Student

class StudentController:
    def __init__(self, csv_file_path):
        self.csv_file_path = 'App/static/studentlog.csv'

    def populate_database_from_csv(self):
        try:
            with open(self.csv_file_path, 'r', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    student = Student(
                        studentID=row['studentID'],
                        studentName=row['studentName'],
                        degree=row['degree'],
                        year=int(row['year']),
                        karma=int(row['karma'])
                    )
                    db.session.add(student)
                db.session.commit()
            return True, "Database populated from CSV successfully"
        except Exception as e:
            return False, str(e)

    def write_students_to_csv(self, csv_file_path):
        try:
            students = Student.query.all()

            with open(csv_file_path, 'w', newline='') as csv_file:
                fieldnames = ['studentID', 'studentName', 'degree', 'year', 'karma']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

                for student in students:
                    writer.writerow({
                        'studentID': student.studentID,
                        'studentName': student.studentName,
                        'degree': student.degree,
                        'year': student.year,
                        'karma': student.karma
                    })

            return True, "Data written to CSV file successfully"
        except Exception as e:
            return False, str(e)

    def add_student(self, studentID, studentName, degree, year, karma):
        try:
            student = Student(studentID=studentID, studentName=studentName, degree=degree, year=year, karma=karma)
            db.session.add(student)
            db.session.commit()
            return True, "Student added successfully"
        except Exception as e:
            return False, str(e)

    def get_student_by_id(self, studentID):
        student = Student.query.filter_by(studentID=studentID).first()
        return student

    def get_students_by_name(self, studentName):
        students = Student.query.filter(Student.studentName == studentName).all()
        return students

    def get_all_students(self):
        students = Student.query.all()
        return students

    def update_student(self, studentID, studentName, degree, year, karma):
        try:
            student = Student.query.filter_by(studentID=studentID).first()
            student.studentName = studentName
            student.degree = degree
            student.year = year
            student.karma = karma
            db.session.commit()
            return True, "Student updated successfully"
        except Exception as e:
            return False, str(e)

    def update_karma(self, studentID, karma, score):
        try:
            student = Student.query.filter_by(studentID=studentID).first()
            student.karma = karma + score
            db.session.commit()
            return True, "Student updated successfully"
        except Exception as e:
            return False, str(e)

    def delete_student(self, studentID):
        try:
            student = Student.query.filter_by(studentID=studentID).first()
            db.session.delete(student)
            db.session.commit()
            return True, "Student deleted successfully"
        except Exception as e:
            return False, str(e)
