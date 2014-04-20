from app import app, db
from flask import request, json, session
from helpers import log, send_json
from business import user

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
