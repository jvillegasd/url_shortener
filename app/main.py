import redis
import json
import string
from random import choice
from flask import request, redirect
from flask_restx import Namespace, Resource, abort, fields
from app.db.db_connection import redis_params
from datetime import datetime

main_namespace = Namespace('url-shortener', description='url shortener')
add_url_model = main_namespace.model('Add url', {'url': fields.String, 'custom_name': fields.String}) 
redis_db = redis.StrictRedis(**redis_params)

@main_namespace.route('/')
@main_namespace.route('/<hash>')
class Home(Resource):
  def get(self, hash=None):
    if hash == 'db':
      redis_all = []
      redis_all.append(redis_db.hgetall('links'))
      redis_all.append(redis_db.hgetall('time'))
      return redis_all
    elif not hash:
      return {'message': 'hello to url shortener'}
    else:
      url = hashToUrl(hash)
      if url:
        lastUsed(url)
        return redirect(url, code=302)
      else:
        return {'message': 'url does not exists'}

@main_namespace.route('/short')
class Short(Resource):
  @main_namespace.expect(add_url_model)
  def post(self):
    params = request.get_json()
    url = params['url']
    custom_name = params['custom_name']
    if custom_name:
      db_url = hashToUrl(custom_name)
      if not db_url:
        new_url = custom_name
      else:
        return {'message': 'custom name already exists'}
    else:
      new_url = getHash()
    redis_db.hset('links', new_url, url)
    lastUsed(new_url)
    return {'new_url': new_url}

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