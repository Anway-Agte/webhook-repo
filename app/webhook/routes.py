from flask import Blueprint, json, request, render_template
from app.extensions import mongo
import enum
import random
from datetime import datetime

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# Data format for converting timestamp
format = "%d %b %Y %I %p"

# Enum for type of request


class Event(enum.Enum):
    PUSH = 1
    PULL = 2
    MERGE = 3

# UI Page where recent activity will be displayed


@webhook.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Endpoint route
@webhook.route('/receiver', methods=["POST", "GET"])
def receiver():
    if request.method == "POST":

        if request.headers["Content-Type"] == "application/json":

            eventData = dict(request.json)

            # dictionary to contain necessary event information

            event = {}

            if "pull_request" in eventData.keys():

                # Checking if pull request is opened
                if eventData["action"] == "opened":

                    event = {
                        # Getting data about the pull request
                        "request_id": eventData["pull_request"]["id"],

                        "author": eventData["sender"]["login"],

                        "action": Event(2).name,

                        "from_branch": eventData["pull_request"]["head"]["ref"],

                        "to_branch": eventData["pull_request"]["base"]["ref"],

                        "timestamp": eventData["pull_request"]["created_at"],

                        # Flag to check if the event recently occured or not .
                        "new": True,

                    }

                    # Converting timestamp to required format
                    tempData = datetime.strptime(
                        event["timestamp"], "%Y-%m-%dT%H:%M:%SZ")

                    event["timestamp"] = tempData.strftime(format)

                    # Inserting event into database
                    if mongo.db.event.insert_one(event):

                        return "Entry successful", 200

                    else:

                        return "There was some error", 400

                # Checking if the pull request was merged
                elif eventData["action"] == "closed" and eventData["pull_request"]["merged"]:

                    if eventData["pull_request"]["merged"] == True:

                        event = {
                            # Getting data about the pull request
                            "request_id": eventData["pull_request"]["id"],

                            "author": eventData["sender"]["login"],

                            "action": Event(3).name,

                            "from_branch": eventData["pull_request"]["head"]["ref"],

                            "to_branch": eventData["pull_request"]["base"]["ref"],

                            "timestamp": eventData["pull_request"]["created_at"],

                            "new": True,

                        }
                        tempData = datetime.strptime(
                            event["timestamp"], "%Y-%m-%dT%H:%M:%SZ")

                        # Formatting date time
                        event["timestamp"] = tempData.strftime(format)

                        # Inserting into databse

                        if mongo.db.event.insert_one(event):

                            return "Entry successful", 200

                        else:

                            return "There was some error", 400

            # Checking for push event in received request
            elif "pusher" in eventData.keys():

                event = {
                    "request_id": eventData["commits"][0]["id"],

                    "author": eventData["pusher"]["name"],

                    "action": Event(1).name,

                    "from_branch": eventData["ref"].split("/")[-1],

                    "to_branch": eventData["ref"].split("/")[-1],

                    "timestamp": eventData["repository"]["pushed_at"],

                    "new": True,

                }

                tempTimeStamp = datetime.fromtimestamp(event["timestamp"])

                # Coverting timestamp into required format
                event["timestamp"] = tempTimeStamp.strftime(format)

                # Inserting into database
                if mongo.db.event.insert_one(event):

                    return "Entry successful", 200

                else:

                    return "There was some error", 400

    return {}, 200

# Route which fetches data from database when called upon by ajax


@webhook.route("/getEvents/", methods=["POST"])
def getEvents():
    events = {}
    if request.method == "POST":
        events = list(mongo.db.event.find({"new": True}))

        for event in events:

            mongo.db.event.find_one_and_update(
                {"_id": event["_id"]}, {'$set': {"new": False}}, )

    return render_template("events.html", events=events)
