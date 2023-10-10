import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, update_user,add_student,
 update_student,update_karma,delete_student,get_all_students,get_student_by_id, add_review, list_review_log_json )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_user('sarah', 'sarahpass')
    add_student('Jane', 'CS', '1', '0')

    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 


# this command will be : flask user create bob bobpass
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user list
@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

#this command will be : flask user update 1 Josiah
@user_cli.command("update", help="Updates a username")
@click.argument("id", default= 1)
@click.argument("username", default = "bob")
def update_user_command(id,username):
    update_user(id,username)
    print(f'{username} updated')

app.cli.add_command(user_cli) # add the group to the cli

'''
Student Commands
'''

student_cli = AppGroup('student', help='Student object cli commands')

# this command will be : flask student add Jane Chemistry 2 0
@student_cli.command("add", help = "Adds a student object to the application")
@click.argument("studentName", default = "Rob")
@click.argument("degree", default = "Biology")
@click.argument("year", default = 1)
@click.argument("karma", default = 0)
def add_student_command(studentname, degree, year, karma):
    student = add_student(studentname, degree, year, karma)
    print(student)
    if student:
        print("student added")
    else:
        print("Error: student was not added")

#this command will be : flask student update 1 Robert Chemistry 3 0
@student_cli.command('update', help = "Updates a student object in the application")
@click.argument("studentID", default = "1")
@click.argument("studentName", default = "Rob")
@click.argument("degree", default = "Biology")
@click.argument("year", default = 1)
@click.argument("karma", default = 0)
def update_student_command(studentid,studentname, degree, year, karma):
    student = update_student(studentid, studentname, degree, year, karma)
    if student:
        print("student updated")
    else:
        print("Error: student was not updated")
    
# this command will be : flask student update_karma 123 0 1
@student_cli.command('update_karma', help = "Updates a students karma score")
@click.argument("studentID", default = "1")
@click.argument("karma", default = 0)
@click.argument("score", default = 1)
def updatekarma_student_command(studentid, karma, score):
    karma = update_karma(studentid,karma,score)
    if karma:
        print("karma updated")
    else:
        print("Error: karma was not updated")
    
#this command will be : flask student delete 123
@student_cli.command('delete', help = "Deletes a student that was to the application")
@click.argument("studentID", default = "1")
def delete_student_command(studentid):
    deleted = delete_student(studentid)
    if deleted:
        print("student deleted")
    else:
        print("Error: student was not updated")

#this command will be : flask student list
@student_cli.command('list', help = "Lists all students that were added to the application")
def list_student_command():
    print(get_all_students())

#this command will be : flask student list_by_id 1
@student_cli.command('list_by_id', help = "Lists student by id that were added to the application")
@click.argument("studentID", default = "1")
def list_student_by_name_command(studentid):
    print(get_student_by_id(studentid))

app.cli.add_command(student_cli) # add the group to the cli

'''
Rating Commands
'''
rating_cli = AppGroup('rating', help='Rating object cli commands')

#this command will be : flask rating add 1 1 good_student student_is_performing_well
@rating_cli.command("add", help = 'Adds a rating to a particular student')
@click.argument("sid", default = "1")
@click.argument("uid", default = "1")
@click.argument("title", default = "Rating")
@click.argument("description", default = "Student is well behaved")
def add_rating_command(sid,uid,title,description):
    rating = add_review(sid, uid, title, description)
    print(rating)
    if rating:
        print("student review created")
    else:
        print("Error: student review not created (WSGI)")

#this command will be : flask rating list
@rating_cli.command("list", help = 'Rating object cli commands')
def list_rating_command():
    print(list_review_log_json())

"""#this command will be : flask rating list 11
@rating_cli.command("list", help = 'Rating object cli commands')
@click.argument("sID", default = "1")
def list_rating_command(sid):
    print(list_review_log_json(sid))"""


    
app.cli.add_command(rating_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)