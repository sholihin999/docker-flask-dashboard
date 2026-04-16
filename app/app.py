from flask import Flask, jsonify, render_template
import redis
import os
import socket

app = Flask(__name__)

redis_host = os.environ.get('REDIS_HOST', 'redis')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.route('/')
def home():
    try:
        count = r.incr('counter')
    except:
        count = 0
    return render_template("index.html", count=count, hostname=socket.gethostname())

@app.route('/api')
def api():
    try:
        count = r.get('counter') or 0
    except:
        count = 0
    return jsonify({"counter": int(count)})

@app.route('/health')
def health():
    return "OK", 200

@app.route('/reset', methods=['POST'])
def reset():
    r.delete('counter')
    return {"counter": 0}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
