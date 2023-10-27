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
        student = Student("Jane", "CS", 4, 12)
        student_json = student.get_json()
        self.assertDictEqual(student_json, {
            "studentID": None ,
            "studentName": "Jane",
            "degree": "CS",
            "year": 4,
            "karma": 12,
        })

    def test_update_student(self):
        student = Student("John Doe", "Computer Science", 1, 16)
        student.studentName = "Jane Smith"
        student.degree = "Software Engineering"
        student.year = 3
        student.karma = 9
        # Now the student's attributes are updated
        self.assertEqual(student.studentName, "Jane Smith")
        self.assertEqual(student.degree, "Software Engineering")
        self.assertEqual(student.year, 3)
        self.assertEqual(student.karma, 9)


    def test_update_karma(self):
        student = Student("Alice Smith", "Data Science", 4, 13)
        student.karma = 5  # Assign a new value to the karma attribute
        self.assertEqual(student.karma, 5)

 

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
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

#class RatingIntegrationTests(unittest.TestCase):
    
    #def test_add_review(self):
     #   pass

class StudentIntegrationTests(unittest.TestCase):
    def test_add_student(self):
        assert add_student("John_Doe", "Computer Science", 2, 88) == (True, 'Student added successfully')
        

    def test_get_student_by_id(self):
        student = get_student_by_id(1)
        assert {'studentID': 1, 'studentName': 'John Doe', 'degree': 'Computer Science', 'year': 2, 'karma': 88}, student


    def test_get_students_by_name(self):
        student = add_student("testman", "Computer Science", 2, 88)
        student = get_students_by_name("testman")
        assert student[0].studentName == "testman"
        assert student[0].degree == "Computer Science"

    def test_get_all_students(self):
        students = get_all_students()
        assert len(students) >= 1  # There should be at least one student in the database

    def test_update_student(self):
        student = add_student("testman", "Computer Science", 2, 88)
        student = get_students_by_name("testman")
        student = student[0]
        assert update_student(student.studentID, studentName="Jane Smith", degree="Software Engineering", year=3, karma=9) == (True, "Student updated successfully")

    def test_update_karma(self):
        add_student("testman", "Computer Science", 2, 88)
        student = get_students_by_name("testman")

        assert update_karma(student[0].studentID, 5) == (True, 'Student updated successfully')

    def test_delete_student(self):
        student = add_student("testman", "Computer Science", 2, 88)
        student = get_students_by_name("testman")
        student_id = student[0].studentID
        assert delete_student(student_id) == (True, "Student deleted successfully")
