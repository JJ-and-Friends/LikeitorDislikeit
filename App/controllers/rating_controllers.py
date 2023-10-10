from datetime import datetime
from App.database import db
from App.models import Rating

def __init__(self, csv_file_path):
    self.csv_file_path = 'App/static/ratinglog.csv'



def add_review(self, sID, userID, title, description):
    try:
        date = datetime.now()
        review = Rating(studentID=sID, userID=userID, title=title, description=description, date=date)
        db.session.add(review)
        db.session.commit()
        self.write_reviews_to_csv()  # Write reviews to CSV after adding
        return True, "Review added successfully"
    except Exception as e:
        return False, str(e)

def list_review_log_json(self, sID):
    try:
        reviews = Rating.query.filter_by(studentID=sID).all()
        review_data = [review.get_json() for review in reviews]
        return review_data
    except Exception as e:
        return False, str(e)

<<<<<<< Updated upstream
def write_reviews_to_csv(self):
    try:
        reviews = Rating.query.all()

        with open(self.csv_file_path, 'w', newline='') as csv_file:
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
=======
def calculate_karma(studentID):
    try:
        # Retrieve all ratings for the student
        ratings = Rating.query.filter_by(studentID=studentID).all()
        
        # Calculate karma based on some logic (for example, the average rating)
        if ratings:
            total_ratings = len(ratings)
            total_rating_value = sum([rating.rating_value for rating in ratings])
            average_rating = total_rating_value / total_ratings
            karma = int(average_rating * 10)  # Example: Scale average rating to a karma value
        else:
            karma = 0  # Default karma if no ratings
        
        return True, karma
>>>>>>> Stashed changes
    except Exception as e:
        return False, str(e)
    
def get_karma():
    try:
        karma = Rating.query.filter_by(karma=karma).all()
        karma_data = [karma.get_json() for karma in karma]
        return karma_data
    except Exception as e:
        return False, str(e)