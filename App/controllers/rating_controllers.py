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



def list_review_log_json():
    try:
        reviews = Rating.query.all()
        return reviews
    except Exception as e:
        return False, str(e)

