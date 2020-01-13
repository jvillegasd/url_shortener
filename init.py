from flask import Flask
from app.main import main_blueprint
from app.jobs.delete_keys import job_blueprint

app = Flask(__name__, template_folder='./app/templates', static_folder='./app/static')
app.register_blueprint(main_blueprint)
app.register_blueprint(job_blueprint)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True)