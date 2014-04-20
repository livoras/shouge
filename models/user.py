from common import db, utils

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(50))

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = utils.encrypt(password)

  def __repr__(self):
    return str(self.json())

  def json(self):
    return {
      'id': self.id,
      'username': self.username, 
      'email': self.email
    }
