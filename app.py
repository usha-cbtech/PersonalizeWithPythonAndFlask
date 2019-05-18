from flask import Flask
from flask import jsonify
from flask import request
import os
import boto3
import json
import time
import io

personalize = boto3.client('personalize')
print("personalize: ", personalize)
personalize_runtime = boto3.client('personalize-runtime')
personalize_events = boto3.client(service_name='personalize-events')

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"



# endpoint to show all users
#/<id> example of path parameter
@app.route("/getSerachResult/<id>", methods=["GET"])
def getSerachResult(id):
    get_recommendations_response = personalize_runtime.get_recommendations(
        campaignArn = "arn:aws:personalize:us-east-1:833408143472:campaign/similler-user-campaign",
        #userId = str(user_id),
        #userId = str(1)
        itemId = str(id)
    )

    print(get_recommendations_response)

    body = {
        "message": "Success",
        "input": get_recommendations_response
    }

    response = {
        "statusCode": 200,
        #"body": json.dumps(body)
        "body": body
    }

    #jsonify(response)
    return jsonify(response)

# endpoint to show all users
#query parameter example
@app.route("/getRecomendedItem", methods=["GET"])
def getRecomendedItem():
    get_recommendations_response = personalize_runtime.get_recommendations(
        campaignArn = "arn:aws:personalize:us-east-1:833408143472:campaign/similler-user-campaign",
        #userId = str(user_id),
        #userId = str(1)
        itemId = str(request.args.get('id'))
    )

    print(get_recommendations_response)

    body = {
        "message": "Success",
        "input": get_recommendations_response
    }

    response = {
        "statusCode": 200,
        #"body": json.dumps(body)
        "body": body

    }

    #jsonify(response)
    return json.dumps(response)
# endpoint to create new user
@app.route("/putInterectionEvent", methods=["POST"])
def putInterectionEvent():
    """POST /events HTTP/1.1
    Content-type: application/json

    {
       "eventList": [
          {
             "eventId": "string",
             "eventType": "string",
             "properties": "string",
             "sentAt": number
          }
       ],
       "sessionId": "string",
       "trackingId": "string",
       "userId": "string"
    } """
    print ("put event call")
    result = personalize_events.put_events(
    trackingId = '15da452e-08cd-4ba8-9f74-a8a968aae34b',
    userId= '1',
    sessionId = 'session_id',
    eventList = [{
        'sentAt': 1234214356,
        'eventType': 'like',
        'properties': json.dumps({
            'itemId': '427',
            'eventValue': 'true'
            })
            }]
        )
    body = {
        "message": "Success",
        "input": result
    }
    print ("put body call")
    response = {
        "statusCode": 200,
        #"body": json.dumps(body)
        "body": body
    }

    #jsonify(response)
    return jsonify(response)

@app.after_request
def after_request(response):
    d = json.loads( response.get_data() )
    #response.set_data( json.dumps(d) )
    return response


#if you want to run locally use -- if __name__ == '__main__':app.run(debug = True)
if __name__ == '__main__':
    #app.run(host = '0.0.0.0', port = 5001, debug = True)
        app.run(debug = True)
