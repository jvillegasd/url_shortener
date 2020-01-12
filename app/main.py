import redis
import json
import string
from random import choice
from flask import request, redirect
from flask_restplus import Namespace, Resource, abort, fields
from app.db.db_connection import redis_params

main_namespace = Namespace('url-shortener', description='url shortener')
add_url_model = main_namespace.model('Add url', {'url': fields.String}) 
redis_db = redis.StrictRedis(**redis_params)

@main_namespace.route('/')
@main_namespace.route('/<hash>')
class Home(Resource):
  def get(self, hash=None):
    if hash == 'db':
      return redis_db.hgetall('links')
    elif not hash:
      return {'message': 'hello to url shortener'}
    else:
      url = hashToUrl(hash)
      if url:
        return redirect(url, code=302)
      else:
        return {'message': 'url does not exists'}

@main_namespace.route('/short')
class Short(Resource):
  @main_namespace.expect(add_url_model)
  def post(self):
    params = request.get_json()
    url = params['url']
    new_url = getHash()
    redis_db.hset('links', new_url, url)
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