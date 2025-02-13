# -*- coding:utf8 -*-
# !/usr/bin/env python


from __future__ import print_function
#from future.standard_library import install_aliases
#install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from myjsondb import REPLIES

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4,sort_keys=True)
    print("#"*100)
    print("NEw modified response")
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    print("Sent Request")
    print(r)
    return r


def processRequest(req):
    print ("here in")
    print(type(req))
    print(req)
    #print(type(req['fulfillmentMessages']))
    try:
        s =  req['queryResult']['intent']['displayName']
    except AttributeError:
        s= "JSON Error"
        
    print ("starting processRequest...",s)
    if(req['queryResult']['intent']['displayName'] != "showBankingProductTypes"):
        print("Check your response intent")
    else:
        print("Intent Verified")
    print("#"*100)
    try:
        d= req['queryResult']['fulfillmentMessages'][1]['payload']['messages'][1]['replies']
    except AttributeError:
        d= "JSON Error in replies"
    
    print("#"*100)
    print("JSON payload to change")
    print(d)
    print(type(d))
    print("#"*100)
    req['queryResult']['fulfillmentMessages'][1]['payload']['messages'][1]['replies'] = REPLIES
    print("New Response")
    print(json.dumps(req, indent=4,sort_keys=True))
    print("#"*100)
    #req = json.dumps(, indent = 4,sort_keys=True)
    #print("Replies payload activated")
    #for i in REPLIES:
    #    print(i)
    #result.metadata.intentName
    """
    if req.get("result").get("metadata").get("intentName") != "showBankingProductTypes":
        print ("Please check your action name in DialogFlow...")
        return req
    #result.fulfillment.messages[1].payload.messages[1].replies = REPLIES
    req['result']['fulfillment']['messages'][1]['payload']['messages'][1]['replies'] = REPLIES
    """
    """
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    print("1.5 1.5 1.5")
    yql_query = makeYqlQuery(req)
    print ("2222222222")
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    print("3333333333")
    print (yql_url)
    
    #result = urlopen(yql_url).read()
    #data = json.loads(result)
    #for some the line above gives an error and hence decoding to utf-8 might help
    #data = json.loads(result.decode('utf-8'))
    #print("44444444444")
    #print (data)
    #res = makeWebhookResult(data)
    """
    return req


def makeSqlQuery(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None
    return "select * from  where text='" + city + "')"


def makeWebhookResult(data):
    print ("starting makeWebhookResult...")
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))

    speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
             ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)
    return {

    "fulfillmentText": speech,
     "source": "Yahoo Weather"
    }


@app.route('/test', methods=['GET'])
def test():
    return  "Hello there my friend !!"


@app.route('/static_reply', methods=['POST'])
def static_reply():
    speech = "Hello there, this reply is from the webhook !! "
    string = "You are awesome !!"
    Message ="this is the message"

    my_result =  {

    "fulfillmentText": string,
     "source": string
    }

    res = json.dumps(my_result, indent=4)

    r = make_response(res)

    r.headers['Content-Type'] = 'application/json'
    return r



if __name__ == '__main__':


    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0', threaded=True)
