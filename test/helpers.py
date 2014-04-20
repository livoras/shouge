import sys
from flask import json

def log(data):
  sys.stdout.write(data)

def send_json(method, url, data, c):
  send_fn = getattr(c, method)
  json_data = json.dumps(data)
  headers = {'Content-Type': 'application/json'}
  return send_fn(url, headers=headers, data=json_data)
