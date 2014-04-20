# -*- coding: utf-8 -*-
import os
from blueprints.user import user_bp
from flask import Flask, render_template

app = Flask(__name__, template_folder='static/app/build/')

blueprints_list = [user_bp]
for bp in blueprints_list:
  app.register_blueprint(bp)

@app.route('/')
def index():
  subtitle = u'你就是一个艺术家'
  return render_template('index.html', subtitle=subtitle)

if __name__ == '__main__':
  app.run(debug=True)