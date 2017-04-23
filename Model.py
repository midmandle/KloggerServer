import time
from google.appengine.ext import ndb


class Session(ndb.Model):
    UserID = ndb.IntegerProperty()
    StartTime = ndb.FloatProperty()
    EndTime = ndb.FloatProperty()

class KeyboardEvent(ndb.Model):
    Window = ndb.StringProperty()
    WindowName = ndb.StringProperty()
    WindowProcName = ndb.StringProperty()
    Key = ndb.StringProperty()
    Ascii = ndb.IntegerProperty()
    KeyID = ndb.BooleanProperty()
    ScanCode = ndb.IntegerProperty()
    MessageName = ndb.StringProperty()
    Time = ndb.FloatProperty()

class MouseEvent(ndb.Model):
    Window = ndb.StringProperty()
    WindowName = ndb.StringProperty()
    WindowProcName = ndb.StringProperty()
    Position = ndb.StringProperty()
    MessageName = ndb.StringProperty()
    Time = ndb.FloatProperty()

class DataObject:
    "'class to hold the data in object form.'"

    def __init__(self, json_content):
        self.endTime = json_content['endTime']
        self.startTime = json_content['startTime']
        self.events = json_content['data']
        self.id = json_content['id']

def storeEvent(dataObj):
    #print dataObj
    session = Session(UserID = dataObj.id, StartTime = dataObj.startTime, EndTime = dataObj.endTime)
    session.put();
    actionsList = []
    for item in dataObj.events:
        eventType = item[0]
        eventData = item[1]
        eventTime = item[2]
        if(eventType == "kb"):
            action = KeyboardEvent(parent = session.key, Window = eventData['Window'], WindowName = eventData['WindowName'], WindowProcName = eventData['WindowProcName'], Key = eventData['Key'], Ascii = eventData['Ascii'], KeyID = eventData['KeyID'], ScanCode = eventData['ScanCode'], MessageName = eventData['MessageName'], Time = eventTime)
            actionsList.append(action)
        if(eventType == "mo"):
            action = MouseEvent(parent = session.key, Window = eventData['Window'], WindowName = eventData['WindowName'], WindowProcName = eventData['WindowProcName'], Position = str(eventData['Position']), MessageName = eventData['MessageName'], Time = eventTime)
            actionsList.append(action)
            #action.put()
    ndb.put_multi(actionsList)


def deleteAll():
    keysList = []
    q = Session.query()
    for i in q:
        keysList.append(i.key)
    ndb.delete_multi(keysList)
    return


def generateSessionData():
    q = Session.query()
    q = q.order(Session.StartTime)
    r = q.fetch();

    list = []

    for i in r:
        dict = {}
        dict["UserID"] = i.UserID
        dict["StartTime"] = time.asctime(time.localtime(i.StartTime))
        dict["EndTime"] = time.asctime(time.localtime(i.EndTime))
        list.append(dict)

    return list

def findSession(id, startTime, endTime):
    startTimeObj = time.mktime(time.strptime(startTime, '%a %b %d %H:%M:%S %Y'))
    endTimeObj = time.mktime(time.strptime(endTime, '%a %b %d %H:%M:%S %Y'))
    idIntegerObj = int(id)

    sessions = Session.query(Session.UserID == idIntegerObj).fetch()

    for session in sessions:
        if(int(session.StartTime) == startTimeObj) and (int(session.EndTime) == endTimeObj):
            return session.key #output;

def findSessionForUser(id):
    sessions = Session.query(Session.UserID == id).order(-Session.StartTime).fetch()
    return sessions

def getAllUserIDs():
    userIDs = []
    sessions = Session.query().order(Session.UserID).fetch()
    for session in sessions:
        if not session.UserID in userIDs:
            userIDs.append(session.UserID)
    return userIDs

def convertItemToDict(item):
    if type(item) == KeyboardEvent:
        dict = {}
        dict["Window"] = item.Window
        dict["WindowName"] = item.WindowName
        dict["WindowProcName"] = item.WindowProcName
        dict["Key"] = item.Key
        dict["Ascii"] = item.Ascii
        dict["KeyID"] = item.KeyID
        dict["ScanCode"] = item.ScanCode
        dict["MessageName"] = item.MessageName
        dict["Time"] = item.Time
        return dict
    elif type(item) == MouseEvent:
        dict = {}
        dict["Window"] = item.Window
        dict["WindowName"] = item.WindowName
        dict["WindowProcName"] = item.WindowProcName
        dict["Position"] = item.Position
        dict["MessageName"] = item.MessageName
        dict["Time"] = item.Time
        return dict
    else:
        return {}
