from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/coordinates', methods = ['GET'])
def getCoords():
    return jsonify({'lat': 57.054, 'lon': 9.912})


if __name__ == '__main__':
    app.run()
