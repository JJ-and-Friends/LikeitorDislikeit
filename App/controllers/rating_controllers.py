from datetime import datetime
from App.database import db
from App.models import Rating


def add_review(sID, userID, title, description):
    try:
        date = datetime.now()
        review = Rating(studentID=sID, userID=userID, title=title, description=description, date=date)
        db.session.add(review)
        db.session.commit()
        return True, "Review added successfully"
    except Exception as e:
        return False, str(e)



def list_review_log_json(sID):
    try:
        reviews = Rating.query.filter_by(studentID=sID).all()
        review_data = [review.get_json() for review in reviews]
        return review_data
    except Exception as e:
        return False, str(e)

