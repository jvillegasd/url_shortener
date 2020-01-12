import redis
import json
import string
from random import choice
from flask import request
from flask_restplus import Namespace, Resource, abort, fields
from app.db.db_connection import redis_params

main_namespace = Namespace('url-shortener', description='url shortener')
add_url_model = main_namespace.model('Add url', {'url': fields.String}) 
redis_db = redis.StrictRedis(**redis_params)

@main_namespace.route('/')
class Home(Resource):
  def get(self):
    return redis_db.hgetall('links')

@main_namespace.route('/short')
class short(Resource):
  @main_namespace.expect(add_url_model)
  def post(self):
    params = request.get_json()
    url = params['url']
    new_url = hashUrl()
    redis_db.hset('links', new_url, url)
    return {'new_url': new_url}

def hashUrl():
  letters = string.ascii_lowercase + string.ascii_uppercase
  new_url = ''
  while True:
    new_url = ''.join(choice(letters) for i in range(6))
    result = redis_db.hget('links', new_url)
    if not result:
      break
  return new_url