import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.database import db, create_db
from App.models import Student, Rating
from App.controllers import(
    #Rating controllers
    add_review,
    list_review_log_json,
    #Student controllers
    add_student,
    get_student_by_id,
    get_students_by_name,
    get_all_students,
    update_student,
    update_karma,
    delete_student
)

''' Unit Tests '''

class RatingUnitTests(unittest.TestCase):
    