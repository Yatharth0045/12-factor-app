from dotenv import load_dotenv
from flask import Flask
from redis import Redis
import os

load_dotenv()

app = Flask(__name__)
redisDb = Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'])

visitCount = 0

@app.route('/')
def mainapp():
    redisDb.incr('visitCount')
    visitCount = redisDb.get('visitCount').decode('utf-8')
    return 'Hello, World! This page has been visited {} times'.format(visitCount)  

if __name__ == '__main__':
    app.run(host=os.environ['APP_HOST'], debug=True, port=os.environ['APP_PORT'])
