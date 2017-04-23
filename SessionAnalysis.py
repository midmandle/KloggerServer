from Model import *

class SessionAnalysis:
    def __init__(self, sessionKey):
        self.sessionKey = sessionKey
        self.keyPresses = KeyboardEvent.query(ancestor=sessionKey).order(KeyboardEvent.Time).fetch()
        self.mouseClicks = MouseEvent.query(ancestor=sessionKey).order(MouseEvent.Time).fetch()

    def sessionTimeline(self):
        timeLine = []
        #label as KeyPress
        for item in self.keyPresses:
            timeLine.append({"kb": convertItemToDict(item)})
        #label as MouseClick
        for item in self.mouseClicks:
            timeLine.append({"mo": convertItemToDict(item)})
        #Sort into combined list based on time.
        output = sorted(timeLine, key=lambda item: item.values()[0]['Time'])
        return output

    def sessionTotalActions(self):
        totalNoActions = len(self.keyPresses) + len(self.mouseClicks)
        return totalNoActions

    def sessionTotalKeyPress(self):
        return len(self.keyPresses)

    def sessionTotalMouseClicks(self):
        return len(self.mouseClicks)

    def sessionListOfPrograms(self):
        programList = []
        timeline = self.sessionTimeline()

        for item in timeline:
            key,value = item.popitem()
            if not value["WindowProcName"] in programList:
                programList.append(value["WindowProcName"])

        return programList

    def sessionTimeSpentPerProgram(self):
        #Returns dictionary of program names and time spent on each.
        programList = self.sessionListOfPrograms()
        timeLine = self.sessionTimeline()
        programDict = dict.fromkeys(programList, 0)

        recent = timeLine[0].values()[0]["Time"]
        for item in timeLine:
            timeSpent = item.values()[0]["Time"] - recent
            recent = item.values()[0]["Time"]
            programDict[item.values()[0]["WindowProcName"]] += timeSpent

        return programDict

    def sessionActionsPerProgram(self):
        programList = self.sessionListOfPrograms()
        timeLine = self.sessionTimeline()
        programDict = dict.fromkeys(programList, 0)

        for item in timeLine:
            programDict[item.values()[0]["WindowProcName"]] += 1

        return programDict

    def sessionKeypressesPerProgram(self):
        programList = self.sessionListOfPrograms()
        programDict = dict.fromkeys(programList, 0)

        for item in self.keyPresses:
            programDict[item.WindowProcName] += 1

        return programDict

    def sessionMouseClicksPerProgram(self):
        programList = self.sessionListOfPrograms()
        programDict = dict.fromkeys(programList, 0)

        for item in self.mouseClicks:
            programDict[item.WindowProcName] += 1

        return programDict


    def sessionTotalTimeSpentSession(self):
        sessionData = Session.get_by_id(self.sessionKey.id())
        timeOut = sessionData.EndTime - sessionData.StartTime
        timeOut = time.strftime("%H %M %S", time.localtime(timeOut))
        return timeOut
