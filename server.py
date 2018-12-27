#!/usr/local/bin/python3.7

# Simple Flask Server with one post route
from flask import Flask, abort, request
import json

app = Flask(__name__)

# simple post route


@app.route('/api/post', methods=['POST'])
def index():
    # api key being passed in as a header
    # abort with a 401 unauthorized error if the api key is not present or incorrect
    api_key = request.headers['x-api-key']
    if api_key != "test123":
        abort(401)

    # abort with a 400 bad error if there is no payload
    if not request.json["payload"] or request.json["payload"] == "" or request.json["payload"] == None:
        abort(400)

    return json.dumps(request.json)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
