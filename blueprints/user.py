from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/<name>', defaults={'name': 'fuckyou'})
def show_name(name):
  data = {'name': name}
  return jsonify(**data)
