from app import app, db
from flask import request, json, session
from helpers import log, send_json
from business import user
from models.user import User
from common import utils

cli = None

def setup(self):
  global cli
  cli = app.test_client()
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  app.testing = True
  db.create_all()


def test_index():
  rv = cli.get('/')
  assert '404' in rv.data


def test_signup():
  data = {'username': 'jerry', 'password': '1343124312', 'email': 'jfuck'}
  with app.test_client() as c:
    rv = send_json('post', '/user/signup', data, c)
    new_user = eval(session['user'])
    assert new_user['username'] == 'jerry'
    assert new_user['info'] == ''
    assert new_user['avatar'] == 'default.jpg'
    assert session['is_login'] == True
    assert 'success' in rv.data  


def test_user_list():
  rv = cli.get('/user/list')
  assert ('<li>' in rv.data)


def test_check_is_login():
  with app.test_client() as c:
    with c.session_transaction() as sess:
      sess['is_login'] = True
      sess['user'] = '{}'

    rv = c.get('/user/check_login')
    assert 'true' in rv.data

    with c.session_transaction() as sess:
      sess['is_login'] = False
    rv = c.get('/user/check_login')
    assert 'false' in rv.data


def test_logout():
  with app.test_client() as c:
    with c.session_transaction() as sess:
      sess['is_login'] = True
    rv = c.delete('/user/logout')  
    assert 'success' in rv.data
    assert session.get('is_login', False) == False


def test_login():
  user_data = {
    'username': 'livoras', 
    'email': 'livoras@163.com', 
    'password': 'fuckyoueveryday'
  }
  user.add_new_user(user_data)

  data = {'email': 'livoras@163.com', 'password': 'fuckyoueveryday'}
  with app.test_client() as c:
    rv = send_json('post', '/user/login', data, c)
    assert 'success' in rv.data
    assert session['is_login'] == True
    assert rv.status_code == 200

    data['email'] = 'fuckcyou@163.com'
    rv = send_json('post', '/user/login', data, c)
    assert 'failed' in rv.data
    assert 'not correct' in rv.data
    assert session.get('is_login', False) == False
    assert rv.status_code == 401

    data['email'] = 'livoras@163.com'
    data['password'] = 'shit'
    rv = send_json('post', '/user/login', data, c)
    assert 'failed' in rv.data
    assert 'not correct' in rv.data
    assert session.get('is_login', False) == False
    assert rv.status_code == 401


def test_update_user():
  with app.test_client() as c:
    with c.session_transaction() as sess:
      sess['is_login'] = True
      sess['user'] = '{"id": "1", "username": "livoras"}'

    rv = send_json('put', '/user/update', {'username': 'lucy', 'info': '233333', 'gender': 'u'}, c) 
    assert 'success' in rv.data
    assert 'lucy' in rv.data
    assert '233333' in rv.data
    assert 'lucy' in session['user']

    # There would be no error if the update name is the same as your name
    rv = send_json('put', '/user/update', {'username': 'lucy', 'info': '233333', 'gender': 'f'}, c) 
    assert 'success' in rv.data

    rv = send_json('put', '/user/update', {'username': 'lucy', 'info': '233333', 'gender': 'c'}, c) 
    assert 'gender is not valid' in rv.data

    rv = send_json('put', '/user/update', {'username': '', 'info': '233333', 'gender': 'c'}, c) 
    assert 'username is not valid' in rv.data

    user_data = {
      'username': 'new_user', 
      'email': 'new_user@163.com', 
      'password': 'fuckyoueveryday'
    }
    user.add_new_user(user_data)

    # conflict username should return 409
    rv = send_json('put', '/user/update', {'username': 'new_user', 'info': '233333', 'gender': 'c'}, c) 
    assert 'username has been used' in rv.data
    assert rv.status_code == 409

    # not login should return 401
    with c.session_transaction() as sess:
      sess['is_login'] = False

    rv = send_json('put', '/user/update', {'username': 'lucy', 'info': '233333', 'gender': 'u'}, c) 
    assert 'user not login' in rv.data
    assert rv.status_code == 401


def test_update_password():
  with app.test_client() as c:

    with c.session_transaction() as sess:
      sess['is_login'] = True
      sess['user'] = '{"id": "1"}'

    rv = send_json('put', '/user/update_password', {"oldPassword": "123456", "newPassword": "12345"}, c)  
    assert 'failed' in rv.data
    assert 401 == rv.status_code

    rv = send_json('put', '/user/update_password', {"oldPassword": "1343124312", "newPassword": "1"}, c)
    assert 'failed' in rv.data
    assert 400 == rv.status_code

    rv = send_json('put', '/user/update_password', {
      "oldPassword": "1343124312",
      "newPassword": "newpassword"}, c)

    user = User.query.filter_by(id="1").first()
    assert 'success' in rv.data
    assert 200 == rv.status_code
    assert user.password == utils.encrypt('newpassword')
