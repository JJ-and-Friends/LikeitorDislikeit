from App.database import db

class Rating(db.Model):
    ratingID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.String(10), db.ForeignKey('student.studentID'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String(256), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    
    def __init__(self, ratingID, title, description, date):
        self.ratingID = ratingID
        self.title = title
        self.description = description
        self.date = date
    
    def get_json(self):
        return{
            'ratingID': self.ratingID,
            'studentID': self.studentID,
            'userID': self.userID,
            'title': self.title,
            'description': self.description,
            'rating': self.rating,
            'date': self.date
        }