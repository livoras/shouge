# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template

app = Flask(__name__, template_folder='static/app/build/')

@app.route('/')
def index():
  subtitle = u'你就是一个艺术家'
  return render_template('index.html', subtitle=subtitle)

if __name__ == '__main__':
  app.run(debug=True)