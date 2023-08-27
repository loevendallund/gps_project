from flask import Flask, jsonify, request, render_template, g
from gps import GPSModule
from flask_redis import FlaskRedis
import redis

app = Flask(__name__)
#redis = FlaskRedis(app)

r = redis.Redis(host='localhost', decode_responses=True)

@app.route('/')
def index():
    return render_template('index.html')

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
    gps = GPSModule(redis_inst=r)
    app.run(debug=True, host="0.0.0.0")
