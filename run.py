import pymongo
from flask import Flask
#from flask_mongoengine import MongoEngine
from extensions import db
from app.services.singup import signup_blueprint
from app.services.user import user_blueprint
#from config import Config
#import os
#from dotenv import load_dotenv

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'Services',
    'host': 'localhost',
    'port': 27017
}

#db = MongoEngine()
#MONGO_URI = os.environ.get('MONGO_URI')

db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello World!!'

app.register_blueprint(signup_blueprint)
app.register_blueprint(user_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
