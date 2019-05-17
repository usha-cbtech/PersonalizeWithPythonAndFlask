from flask import Flask
import os
import boto3
import json
import time
import io

personalize = boto3.client('personalize')
print("personalize: ", personalize)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001, debug = True)
