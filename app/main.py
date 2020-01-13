import redis
import json
import string
from cerberus import Validator
from random import choice
from flask import request, redirect, Blueprint, render_template, jsonify
from app.db.db_connection import redis_params
from datetime import datetime

main_blueprint = Blueprint('URL shortener', __name__)
redis_db = redis.StrictRedis(**redis_params)
short_schema = {
  'url': {
    'type': 'string', 
    'required': True,
    'empty': False,
    'regex': '^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
    },
  'custom_name': 
  {'type': 'string', 
  'required': True
  }
}
cerberus_validator = Validator(short_schema)

@main_blueprint.route('/')
def index():
  return render_template('index.html')

@main_blueprint.route('/<hash>', methods=['GET'])
def hashRedirect(hash):
  if hash == 'db':
    redis_all = []
    redis_all.append(redis_db.hgetall('links'))
    redis_all.append(redis_db.hgetall('time'))
    return jsonify(redis_all)
  else:
    url = hashToUrl(hash)
    if url:
      lastUsed(url)
      return redirect(url, code=302)
    else:
      return jsonify({'message': 'url does not exists'})

@main_blueprint.route('/short', methods=['POST'])
def short():
  params = request.get_json()
  if not cerberus_validator(params):
    return jsonify({'message': 'invalid json body'})
  url = params['url']
  custom_name = params['custom_name']
  if custom_name:
    db_url = hashToUrl(custom_name)
    if not db_url:
      new_url = custom_name
    else:
      return jsonify({'message': 'custom name already exists'})
  else:
    new_url = getHash()
  redis_db.hset('links', new_url, url)
  lastUsed(new_url)
  return jsonify({'new_url': new_url})

def getHash():
  letters = string.ascii_lowercase + string.ascii_uppercase
  new_url = ''
  while True:
    new_url = ''.join(choice(letters) for i in range(6))
    result = redis_db.hget('links', new_url)
    if not result:
      break
  return new_url

def hashToUrl(hash):
  result = redis_db.hget('links', hash)
  return result

def lastUsed(url):
  current_time = (datetime.today()).strftime('%d/%m/%Y')
  redis_db.hset('time', url, current_time)