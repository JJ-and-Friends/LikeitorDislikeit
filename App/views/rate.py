
from flask import Blueprint, render_template, jsonify, request, send_from_directory, Flask, redirect, url_for
#from flask_jwt_extended import jwt_required, current_user as jwt_current_user
#from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    add_review,
    list_review_log_json,
)

rate_views = Blueprint('rate_views', __name__, template_folder='../templates')

@rate_views.route('/rate/review', methods=['POST'])
def add_rating():
    try:
        # Get JSON data from the request
        data = request.get_json()
        # Extract the necessary parameters from the JSON data
        sid = data.get('sid')
        uid = data.get('uid')
        title = data.get('title')
        description = data.get('description')

        # Call the controller function to add a review with the extracted data
        success, message = add_review(sid, uid, title, description)

        if success:
            return jsonify({'message': message}), 201  # 201 Created status code for successful addition
        else:
            return jsonify({'error': message}), 400  # 400 Bad Request status code for errors

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # 500 Internal Server Error for unexpected exceptions

@rate_views.route('/rate/get-reviews', methods=['GET'])
def get_reviews():
    try:
        # Call the controller function to get the list of reviews
        reviews = list_review_log_json()

        if reviews:
            reviews_list = [
                {
                    'ratingID': review.ratingID,
                    'studentID': review.studentID,
                    'userID': review.userID,
                    'title': review.title,
                    'description': review.description,
                }
                for review in reviews
            ]
            return jsonify(reviews_list), 200  # 200 OK status code for successful retrieval
        else:
            return jsonify({'error': 'No reviews found'}), 404  # 404 Not Found status code if no reviews found

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # 500 Internal Server Error for unexpected exceptions