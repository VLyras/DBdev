#! /usr/bin/env python

from __init__ import app, db
from models import User, Bookmark, Tag
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

app.config['DEBUG'] = True

#Just to add dummy data. More stuff in 7.6 from training
@manager.command
def insert_data():
    db.create_all()
    db.session.add(User(username="lyras", email="lyras@example.com", password="test"))
    db.session.commit()
    print('Inserted data')


@manager.command
def dropdb():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print('Dropped the database')


if __name__ == '__main__':
    manager.run()
