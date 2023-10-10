from datetime import datetime
from App.database import db
from App.models import Rating
from App.models import Student
from App.models import User


def add_review(sid, uid, title, description):
    try:
        #date = datetime.now()
        """student = Student.query.get(sid)
        user = User.query.get(uid)
        if student and user:
            review = Rating(student.studentID, user.id, title, description)
        else:
            return "could not create review (controller)"""
        review = Rating(sid, uid, title, description)
        db.session.add(review)
        db.session.commit()
        return True, "Review added successfully"
    except Exception as e:
        db.session.rollback()
        return False, "Review could not be added (controller)"



def list_review_log_json():
    try:
        reviews = Rating.query.all()
        return reviews
    except Exception as e:
        return False, str(e)

