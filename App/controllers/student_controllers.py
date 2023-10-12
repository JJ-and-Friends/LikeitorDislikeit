from App.models import Student
from App.database import db



def add_student(studentName, degree, year, karma):
    try:
        student = Student(studentName=studentName, degree=degree, year=year, karma=karma)
        db.session.add(student)
        db.session.commit()
        return True, "Student added successfully"
    except Exception as e:
        return False, str(e)

def get_student_by_id(studentID):
    student = Student.query.filter_by(studentID=studentID).first()
    return student

def get_students_by_name(studentName):
    students = Student.query.filter(Student.studentName == studentName).all()
    return students

def get_all_students():
    students = Student.query.all()
    return students

def update_student(studentID, studentName, degree, year, karma):
    try:
        student = Student.query.filter_by(studentID=studentID).first()
        if student:
            student.studentName = studentName
            student.degree = degree
            student.year = year
            student.karma = karma
            db.session.commit()
            return True, "Student updated successfully"
        else: 
            db.session.rollback()
            return False, "Student does not exist"
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def update_karma(studentID, karma):
    try:
        student = Student.query.filter_by(studentID=studentID).first()
        if student:
            student.karma = karma + student.karma
            db.session.commit()
            return True, "Student updated successfully"
        else: 
            db.session.rollback()
            return False, "Student does not exist"
            
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def delete_student(studentID):
    try:
        student = Student.query.filter_by(studentID=studentID).first()
        db.session.delete(student)
        db.session.commit()
        return True, "Student deleted successfully"
    except Exception as e:
        return False, str(e)
