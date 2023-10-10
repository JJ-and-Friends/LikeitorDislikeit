
from flask import Blueprint, render_template, jsonify, request, send_from_directory, Flask, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from .index import index_views

from App.controllers import (
    add_review,
    list_review_log_json,
)

rate_views = Blueprint('rate_views', __name__, template_folder='../templates')

@rate_views.route('rate/review', methods=['POST'])
def add_rating():
    pass

