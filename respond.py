from flask import Flask, request, redirect, Response
from twilio.twiml.messaging_response import MessagingResponse
import logging
import requests
import re
import config
import routes

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    number = request.form['From']
    message_body = request.form["Body"]
    targets = []
    resp = MessagingResponse()
    if re.search("^bus_.*_.*", message_body):
        targets = re.split("_", message_body)
        targets.pop(0) # remove the bus part

        gresp = getDirections(targets[0], targets[1])
        if gresp != []:
            resp.status_code = 200
            resp.message("Your origin is %s and destination is %s. Then, %s" % (targets[0], targets[1], "".join(steps)))
            #app.logger.warning("Your origin is %s and destination is %s. Then,\n %s" % (targets[0], targets[1], "".join(steps)))
        else:
            resp.status_code = 401
            resp.message("Unable to get directions :(")

    return Response(str(resp), mimetype="application/xml")

@app.route("/websim", methods=["GET"])
def sim_reply():
    orig = request.args["origin"]
    dest = request.args["dest"]

    return "Your origin is %s and destination is %s. Then, %s" % (orig, dest, "".join(getDirections(orig, dest)))

def getDirections(origin, destination):
    gresp = requests.get(routes.GMAPS_ROUTE+"?origin="+origin+"&destination="+destination+"&mode=transit"+"&key="+config.GMAPS_API_KEY)

    steps = []
    leave = arive = ""
    if gresp.status_code == 200:
        gjson = gresp.json()["routes"][0]["legs"][0]
        arrive = gjson["arrival_time"]["text"]
        leave = gjson["departure_time"]["text"]
        for step in gjson["steps"]:
            if step["travel_mode"] != "WALKING":
                transitDetails = step["transit_details"]
                steps.append(
                    transitDetails["line"]["agencies"][0]["name"] + " " + transitDetails["line"]["name"] + " from " + 
                    transitDetails["departure_stop"]["name"] + " at " + transitDetails["departure_time"]["text"] +
                    " to " + transitDetails["arrival_stop"]["name"] + " at " + transitDetails["arrival_time"]["text"] + ". "
                )
    
    return steps

@app.route("/test", methods=['GET', 'POST'])
def test_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response

    number = request.form['From']
    message_body = request.form["Body"]
    resp = MessagingResponse()

    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
