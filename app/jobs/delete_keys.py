import redis
from flask_restplus import Namespace, Resource
from app.db.db_connection import redis_params
from datetime import datetime

job_namespace = Namespace('Delete keys', description='Delete urls after 1 month unused for db storage afford')
redis_db = redis.StrictRedis(**redis_params)

@job_namespace.route('/')
class Job(Resource):
  def get(self):
    current_time = datetime.today()
    for hash, date in redis_db.hgetall('time'):
      print(hash)
      print(date)
    return {'message': 'job done'}