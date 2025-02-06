from dotenv import load_dotenv
from flask import Flask
from redis import Redis
import os

load_dotenv()

app = Flask(__name__)
redisDb = Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'])

@app.route('/')
def adminapp():
    return 'Admin app is running...'
    
@app.route('/cleanup')
def cleanCounter():
    redisDb.set('visitCount', 0)
    return 'Visit count has been reset'

if __name__ == '__main__':
    app.run(host=os.environ['APP_HOST'], debug=True, port=os.environ['APP_PORT'])
