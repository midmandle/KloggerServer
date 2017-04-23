from flask import Flask, request, render_template
import requests
import json
from Model import *
from View import *
from SessionAnalysis import SessionAnalysis


app = Flask(__name__)
app.config['DEBUG'] = True


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/recieveData', methods=['POST', 'GET'])
def recieveClientData():
    #print "'"+request.data+"'"
    if request.get_json():
        content = json.loads(request.get_json())
        dataObj = DataObject(content)
        storeEvent(dataObj)
    else:
        print "No JSON"

    return 'DONE'


@app.route('/')
def index():
    #Previous stuff to filter out text from events.
    #r = generateActionTimeline()
    #processText(r)
    return render_template("indexContent.html", log_content = generateSessionData())

@app.route('/refreshContentLog', methods=['POST'])
def refreshContentLog():
    return json.dumps(generateSessionData())


@app.route('/deleteContentsFromServer', methods=['POST'])
def deleteContentsFromServer():
    deleteAll()
    return "Contents erased."


@app.route('/generateSessionStats', methods=['POST'])
def generateSessionStats():
    if request.get_json():
        content = request.get_json();
        sessionKey = findSession(content["id"], content["startTime"], content["endTime"])
        return returnViewOverviewAndTimeline(sessionKey)
    else:
        print "NON-JSON CONTENT RECIEVED"
        print request.get_json()
        return "NON-JSON CONTENT RECIEVED"

@app.route('/generateUserSessionStats', methods=['POST'])
def generateUserSessionStats():
    if request.get_json():
        content = request.get_json();
        return returnViewUserData(content["id"])
    else:
        print "NON-JSON CONTENT RECIEVED"
        print request.get_json()
        return "NON-JSON CONTENT RECIEVED"

@app.route('/generatePopulationStats', methods=['GET'])
def generatePopulationStats():
    popIDs = getAllUserIDs()
    return returnViewPopulationData(popIDs)


@app.route('/getUsersList', methods=['GET'])
def getUsersList():
    return json.dumps(getAllUserIDs())

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
