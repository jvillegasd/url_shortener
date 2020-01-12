import redis
from flask import Flask, jsonify, Blueprint
from app.db.db_connection import redis_params
from datetime import datetime

job_blueprint = Blueprint('Delete unused url from 28 days job', __name__)
redis_db = redis.StrictRedis(**redis_params)

@job_blueprint.route('/job', methods=['DELETE'])
def delete():
  current_time = datetime.today()
  hash_to_delete = []
  for hash, str_date in redis_db.hgetall('time').items():
    date_obj = datetime.strptime(str_date, '%d/%m/%Y')
    delta = current_time - date_obj
    if delta.days >= 28:
      hash_to_delete.append(hash)
  if hash_to_delete:
    redis_db.hdel('time', *hash_to_delete)
    redis_db.hdel('links', *hash_to_delete)
  return jsonify({'message': 'job done'})