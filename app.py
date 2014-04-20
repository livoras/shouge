from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import common
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

common.db = db
common.app = app

from blueprints.user import user_bp

def register_all_bps():
  buleprints_candidates = (user_bp,)
  for bp in buleprints_candidates:
    app.register_blueprint(bp)

register_all_bps()

if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)
