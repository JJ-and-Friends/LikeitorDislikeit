from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers import (
)

rate_views = Blueprint('rate_views', __name__, template_folder='../templates')

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