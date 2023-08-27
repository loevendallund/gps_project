from flask import Flask, jsonify, request, render_template, g
from gps import GPSModule
from flask_redis import FlaskRedis
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', decode_responses=True)

# Main route to render index, shows a map and coordinates
@app.route('/')
def index():
    return render_template('index.html')

# Api call to fetch the coordinates from redis
@app.route('/api/coordinates', methods = ['GET'])
def getCoords():
    lat = None
    lng = None
    if r.exists("lat"):
        lat = r.get("lat")
    if r.exists("lng"):
        lng = r.get("lng")

    return jsonify({"lat": lat, "lng": lng})

if __name__ == '__main__':
    GPSModule(redis_inst=r)
    app.run(host="0.0.0.0")
