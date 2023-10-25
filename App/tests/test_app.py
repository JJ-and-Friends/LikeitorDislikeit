import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Student, Rating
from App.controllers import(
    #User Teesting
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    #Rating Testing
    add_review,
    list_review_log_json,
    #Student Testing
    add_student,
    get_student_by_id,
    get_students_by_name,
    get_all_students,
    update_student,
    update_karma,
    delete_student,
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)


class RatingUnitTests(unittest.TestCase):
    def test_new_rating(self):
        rating = Rating(1, 1, 'Good Sleep', 'After a great massage, I had a good nap during lunch')
        assert rating.studentID == 1
        assert rating.userID == 1
        assert rating.title == 'Good Sleep'  # Use lowercase 'title'
        assert rating.description == 'After a great massage, I had a good nap during lunch'

    def test_get_json(self):
        rating = Rating(1, 1, 'Good Sleep', 'After a great massage, I had a good nap during lunch')
        rating_json = rating.get_json()
        self.assertDictEqual(rating_json, {
            "ratingID": None,
            "studentID": 1,
            "userID": 1,
            "title": "Good Sleep",  # Use lowercase 'title'
            "description": "After a great massage, I had a good nap during lunch"
        })



class StudentUnitTesting(unittest.TestCase):
    def test_new_student(self):
        student = Student("John Doe", "Computer Science", 2, 88)
        assert student.studentName == "John Doe"
        assert student.degree == "Computer Science"
        assert student.year == 2
        assert student.karma == 88

    def test_get_student_json(self):
        student = Student("Alice Smith", "Data Science", 4, 12)
        student_json = student.get_json()
        self.assertDictEqual(student_json, {
            "studentID": None,
            "name": "Alice Smith",
            "degree": "Data Science",
            "year": 4,
            "karma": 12,
        })

    def test_update_student(self):
        student = Student("John Doe", "Computer Science", 1, 16)
        student.update_student(studentName="Jane Smith", degree="Software Engineering", year=3, karma=9)
        assert student.studentName == "Jane Smith"
        assert student.degree == "Software Engineering"
        assert student.year == 3
        assert student.karma == 9

    def test_update_karma(self):
        student = Student("Alice Smith", "Data Science",4, 13)
        student.update(5)
        assert student.karma == 5
 
    def test_delete_student(self):
        student = Student("Bob Johnson", "Electrical Engineering", 4, 55)
        student_id = student.studentID  # Get the student's ID before deletion
        student.delete(1)




'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'postgresql://software01:IeGSU0VHqiUqOPZzxhM1PFx5s3msxXgz@dpg-ckjeacolk5ic73dh6i40-a.oregon-postgres.render.com/software_eng'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

class RatingIntegrationTests(unittest.TestCase):
    
    def test_add_review(self):
        add_review(1, 1, 'Good Sleep', 'After a great massage, I had a good nap during lunch')
        reviews = list_review_log_json()
        self.assertListEqual([{
            "ratingID": 1,
            "studentID": 1,
            "userID": 1,
            "Title": "Good Sleep",
            "description": "After a great massage, I had a good nap during lunch"
        }], reviews)

class StudentIntegrationTests(unittest.TestCase):
    def test_add_student(self):
        student = add_student("John Doe", "Computer Science", 2, 88)
        assert student.studentName == "John Doe"
        assert student.degree == "Computer Science"
        assert student.year == 2
        assert student.karma == 88

    def test_get_student_by_id(self):
        student = get_student_by_id(1)
        assert student.studentName == "John Doe"
        assert student.degree == "Computer Science"
        assert student.year == 2
        assert student.karma == 88

    def test_get_students_by_name(self):
        students = get_students_by_name("John Doe")
        assert len(students) == 1
        student = students[0]
        assert student.studentName == "John Doe"
        assert student.degree == "Computer Science"

    def test_get_all_students(self):
        students = get_all_students()
        assert len(students) >= 1  # There should be at least one student in the database

    def test_update_student(self):
        student = get_student_by_id(1)
        update_student(student.studentID, studentName="Jane Smith", degree="Software Engineering", year=3, karma=9)
        updated_student = get_student_by_id(1)
        assert updated_student.studentName == "Jane Smith"
        assert updated_student.degree == "Software Engineering"
        assert updated_student.year == 3
        assert updated_student.karma == 9

    def test_update_karma(self):
        student = get_student_by_id(1)
        update_karma(student.studentID, 5)
        updated_student = get_student_by_id(1)
        assert updated_student.karma == 5

    def test_delete_student(self):
        student = get_student_by_id(1)
        student_id = student.studentID
        delete_student(student_id)
        deleted_student = get_student_by_id(student_id)
        assert deleted_student is None