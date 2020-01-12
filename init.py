from flask import Flask
from flask_restplus import Api, Namespace
from app.main import main_namespace

app = Flask(__name__)
api = Api(app=app)
api.add_namespace(main_namespace, path='/api')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True)