from flask import Flask
from redis import Redis

app = Flask(__name__)
redisDb = Redis(host='redis', port=6379)

visitCount = 0

@app.route('/')
def mainapp():
    redisDb.incr('visitCount')
    visitCount = redisDb.get('visitCount').decode('utf-8')
    return 'Hello, World! This page has been visited {} times'.format(visitCount)  

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
