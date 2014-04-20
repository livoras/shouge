from models.user import User
from common import db, utils
from flask import session, jsonify

def is_valid_user_data(data):
  username = data.get('username')
  email = data.get('email')
  password = data.get('password')

  if not username or not (4 <= len(username) <= 30):
    return ['username\'s length should be 4~30']
  if not email or len(email) == 0: 
    return ['email is not valid']
  if not password or not (6 <= len(password) <= 30):
    return ['password\'s length should be between 6 and 30']


def user_no_conflict(data):
  username = data['username']
  email = data['email']

  if User.query.filter_by(email=email).first():
    return ['email has been registered']

  if User.query.filter_by(username=username).first():
    return ['username has been used']


def add_new_user(data):
  new_user = User(**data)
  db.session.add(new_user)
  db.session.commit()
  return new_user


def get_all_users():
  return User.query.all()


def set_session(user):
  session['is_login'] = True
  session['user'] = str(user)


def login(user_data):
  email = user_data.get('email', None)
  password = user_data.get('password', None)
  if not (email and password): return

  password = utils.encrypt(password)
  return User.query.filter_by(email=email, password=password).first()
