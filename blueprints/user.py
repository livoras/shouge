from flask import Blueprint, jsonify, request, abort, session
import business.user as user 

user_bp = Blueprint('user', __name__)


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


@user_bp.route('/user/update', methods=['PUT'])  
def update_user():
  data = request.json

  username = data.get('username')
  info = data.get('info')
  gender = data.get('gender')

  status_code = None
  current_user = None

  if not session['is_login']:
    error = ['user not login']
    status_code = 401
    result = {'result': 'failed', 'error': error}
    return jsonify(**result), status_code
  else:  
    current_user = eval(session['user'])

  if not user.is_username_valid(username):
    error = ['username is not valid']
    status_code = 400
    result = {'result': 'failed', 'error': error}

  elif current_user['username'] != username and user.is_username_exited(username):
    error = ['username has been used']
    status_code = 409
    result = {'result': 'failed', 'error': error}

  elif not user.is_gender_valid(gender):
    error = ['gender is not valid']
    status_code = 400
    result = {'result': 'failed', 'error': error}

  elif not user.is_info_valid(info):
    error = ['information is too long']
    status_code = 400
    result = {'result': 'failed', 'error': error}

  else:  
    new_user = user.update_profile(data)
    user.set_session(new_user)
    status_code = 200
    result = {'result': 'success', 'data': new_user.json()}

  return jsonify(**result), status_code


@user_bp.route('/user/update_password', methods=['PUT'])
def update_password():
  data = request.json
  old_password = data.get('oldPassword')
  new_password = data.get('newPassword')

  status_code = None 

  if not session.get('is_login'):
    error = ['You have to login first']
    result = {'result': 'failed', 'error': error}
    status_code = 401

  elif not user.is_password_correct(old_password):
    error = ['Password is not correct']
    result = {'result': 'failed', 'error': error}
    status_code = 401

  elif not user.is_password_valid(new_password):
    error = ['New password is not valid']
    result = {'result': 'failed', 'error': error}
    status_code = 400

  else:  
    user.update_password(new_password)
    result = {'result': 'success'}
    status_code = 200

  return jsonify(**result), status_code
