from models.user import User
from common import db, utils
from flask import session, jsonify

def is_valid_user_data(data):
  username = data.get('username')
  email = data.get('email')
  password = data.get('password')

  if not is_username_valid(username):
    return ['username\'s length should be 4~30']

  if not is_email_valid(email): 
    return ['email is not valid']

  if not is_password_valid(password):
    return ['password\'s length should be between 6 and 30']

def is_username_valid(username):
  return username and (4 <= len(username) <= 30)

def is_email_valid(email):
  return email and not len(email) == 0 

def is_password_valid(password):
  return password and (6 <= len(password) <= 30)

def is_username_exited(username):
  return User.query.filter_by(username=username).first()

def is_gender_valid(gender):
  return gender in ['f', 'm', 'u']

def is_info_valid(info):
  return len(info) <= 100


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


def update_profile(data):
  current_user = eval(session['user'])
  query = User.query.filter_by(id=current_user['id'])
  query.update(data)
  db.session.commit()
  return query.first()

def update_password(password):
  user = eval(session['user'])
  return User.query.filter_by(id=user['id']).update(dict(password=utils.encrypt(password)))

def is_password_correct(password):
  user = eval(session['user'])
  user = User.query.filter_by(id=user['id']).first()
  return utils.encrypt(password) == user.password

