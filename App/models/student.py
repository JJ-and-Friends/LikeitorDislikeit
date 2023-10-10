from App.database import db

class Student(db.Model):
    studentID = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    karma = db.Column(db.Integer, nullable=False)
    ratings = db.relationship('Rating', backref='student', lazy=True)

    def __init__(self, studentName, degree, year, karma):
        self.studentName = studentName
        self.degree = degree
        self.year = year
        self.karma = karma
    
    def get_json(self):
        return{
            'studentID': self.studentID,
            'studentName': self.studentName,
            'degree': self.degree,
            'year': self.year,
            'karma': self.karma
        }