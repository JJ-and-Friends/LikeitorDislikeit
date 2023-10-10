<<<<<<< Updated upstream
<<<<<<< Updated upstream
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers import (
=======
from flask import Blueprint, render_template, jsonify, requests, send_from_directory, Flask, redirect, url_for
=======
from flask import Blueprint, render_template, jsonify, request, send_from_directory, Flask, redirect, url_for
>>>>>>> Stashed changes
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    add_review,
<<<<<<< Updated upstream
    list_review_log_json
>>>>>>> Stashed changes
=======
    list_review_log_json,
    calculate_karma,
    get_karma
>>>>>>> Stashed changes
)

rate_views = Blueprint('rate_views', __name__, template_folder='../templates')

<<<<<<< Updated upstream
<<<<<<< Updated upstream
'''
Page/Action Routes
'''

# I would like the routes to recieve the data from the db
# example loading the students karma data
# ['Get Requests'] <-- load db data
# ['Get Requests'] <-- load the db student and karma data (most recent)
# ['Get Requests'] <-- generate the top 5 best positve karma score students
# ['Get Requests'] <-- generate the top 5 wordt karma score students
# 
# ['Post Requests'] <-- add a new student to the db
# ['Post Requests'] <-- add a rating to a student
# ['Post Requests'] <-- add a description to the student
#
# ['Put Request'] <-- edit student description
# [''] <--
#
# ['Delete Request'] <-- deletion of a description instance made

@rate_views.route()
=======
>>>>>>> Stashed changes
=======
@rate_views.route('user/review', methods=['POST'])
def add_review_route():
    try:
        data = request.get_json()

        success, message = add_review(data.get('studentID'), data.get('userID'), data.get('title'), data.get('description'))

        if success:
            return jsonify({'message': message}), 201
        else:
            return jsonify({'error': message}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500
 

@rate_views.route('users/show-rating/', methids=['GET'])
def display_data(sID):
    try:
        reviews = Rating.query.filter_by(studentID=sID).all()
        review_data = [review.get_json() for review in reviews]
        return review_data
    except Exception as e:
        return False, str(e)

@rate_views.route('users/karma/', methods=['GET'])
def get_karma_route():
    try:
        karma = Rating.query.filter_by(karma=karma).all()
        karma_data = [karma.get_json() for karma in karma]
        return karma_data
    except Exception as e:
        return False, str(e)
    
@rate_views.route('users/calculate-karma/', methods=['GET'])
def calculate_karma_route():
    try:
        ratings = Rating.query.filter_by(studentID=studentID).all()
        
        if ratings:
            total_ratings = len(ratings)
            total_rating_value = sum([rating.rating_value for rating in ratings])
            average_rating = total_rating_value / total_ratings
            karma = int(average_rating * 10)  # Example: Scale average rating to a karma value
        else:
            karma = 0  # Default karma if no ratings
        
        return True, karma
    except Exception as e:
        return False, str(e)
    
@rate_views.route('users/list-review-log/', methods=['GET'])
def list_review_log_route():
    try:
        reviews = Rating.query.filter_by(studentID=sID).all()
        review_data = [review.get_json() for review in reviews]
        return review_data
    except Exception as e:
        return False, str(e)

>>>>>>> Stashed changes
