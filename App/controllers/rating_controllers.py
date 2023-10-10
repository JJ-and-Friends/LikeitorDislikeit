import csv
from datetime import datetime
from App.database import db
from App.models import Rating


def __init__(self, csv_file_path):
    self.csv_file_path = 'App/static/ratinglog.csv'

def read_from_csv(self):
    try:
        with open(self.csv_file_path, 'r', newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                review = Rating(
                    studentID=row['studentID'],
                    userID=row['userID'],
                    title=row['title'],
                    description=row['description'],
                    date=date
                )
                db.session.add(review)
            db.session.commit()
        return True, "Model populated from CSV successfully"
    except Exception as e:
        return False, str(e)

def add_review(sID, userID, title, description):
    try:
        date = datetime.now()
        review = Rating(studentID=sID, userID=userID, title=title, description=description, date=date)
        db.session.add(review)
        db.session.commit()
        review.write_reviews_to_csv()  # Write reviews to CSV after adding
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

def write_reviews_to_csv():
    try:
        reviews = Rating.query.all()

        with open(reviews.csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['ratingID', 'studentID', 'userID', 'title', 'description', 'date']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for review in reviews:
                writer.writerow({
                    'ratingID': review.ratingID,
                    'studentID': review.studentID,
                    'userID': review.userID,
                    'title': review.title,
                    'description': review.description,
                    'date': review.date
                })

        return True, "Reviews written to CSV file successfully"
    except Exception as e:
        return False, str(e)
