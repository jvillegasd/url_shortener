import redis
from flask_restplus import Namespace, Resource
from app.db.db_connection import redis_params
from datetime import datetime

job_namespace = Namespace('Delete keys', description='Delete urls after 28 days unused for db storage afford')
redis_db = redis.StrictRedis(**redis_params)

@job_namespace.route('/')
class Job(Resource):
  def get(self):
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
    return {'message': 'job done'}