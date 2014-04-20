from flask import Blueprint, jsonify, request, abort, session
import business.user as user 

user_bp = Blueprint('user', __name__)
import sys

@user_bp.route('/user/signup', methods=['POST'])
def signup():
  data = request.json
  error = user.is_valid_user_data(data)
  if not error: error = user.user_no_conflict(data)
  if not error:
    new_user = user.add_new_user(data)
    user.set_session(new_user)
    result = {'result': 'success'}
  else:   
    result = {'result': 'failed', 'error': error}
  return jsonify(**result)


@user_bp.route('/user/list')  
def list_users():
  html = ''
  for each_user in user.get_all_users():
    html = html + '<li>' + str(each_user) + '</li>'
  return html  


@user_bp.route('/user/check_login')
def check_login():
  result = {
    'isLogin': session.get('is_login', False), 
    'data': eval(session.get('user', '{}'))
  }
  return jsonify(**result)


@user_bp.route('/user/logout', methods=['DELETE'])
def logout():
  session.clear()
  result = {'result': 'success'}
  return jsonify(**result)


@user_bp.route('/user/login', methods=['POST'])
def login():
  data = request.json
  login_user = user.login(data)

  if login_user:
    user.set_session(login_user)
    result = {'result': 'success', 'data': login_user.json()}
    status_code = 200
  else:  
    session.clear()
    error = ['username or password is not correct']
    result = {'result': 'failed', 'error': error}
    status_code = 401

  return jsonify(**result), status_code
