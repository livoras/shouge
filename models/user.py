from common import db, utils

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  email = db.Column(db.String(120), unique=True)
  password = db.Column(db.String(50))
  info = db.Column(db.String(100), server_default='')
  avatar_ext = db.Column(db.String(3), server_default='')
  gender = db.Column(db.String(1), server_default='u')

  def __init__(self, username, email, password):
    self.p = password
    self.username = username
    self.email = email
    self.password = utils.encrypt(password)

  def __repr__(self):
    return str(self.json())

  def json(self):
    if self.avatar_ext == '':
      avatar = 'default.jpg'
    else:  
      avatar = utils.encrypt(self.email) + '.' + self.avatar_ext

    return {
      'id': self.id,
      'username': self.username, 
      'email': self.email,
      'info': self.info,
      'avatar': avatar
    }
