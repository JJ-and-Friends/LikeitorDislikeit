import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, update_user,add_student)

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
# this command will be : flask user create bob bobpass
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user list users
@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

#this command will be : flask user update 1 bob
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

# this command will be : flask student add
@student_cli.command("add", help = "Adds a student object to the application")
@click.argument("self", default = None)
@click.argument("studentID", default = 1)
@click.argument("studentName", default = "Jane Doe")
@click.argument("degree", default = "Computer Science")
@click.argument("year", default = 3)
@click.argument("karma", default = 0)
def add_student_command(self,studentID,studentName,degree,year,Karma):
    student = add_student(self,studentID,studentName,degree,year,Karma)
    if student:
        print('Student added')
    else :
        print("Error: student was not added")

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