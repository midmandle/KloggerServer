from Model import *
from SessionAnalysis import SessionAnalysis

class UserAnalysis:
    def __init__(self, userID):
        self.userID = userID
        self.userSessions = findSessionForUser(userID)

    def timeSpentPerSession(self):
        timePerSessionDict = {}
        for session in self.userSessions:
            timeSpent = session.EndTime - session.StartTime
            startDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session.StartTime))
            timePerSessionDict[startDateTime] = timeSpent

        return timePerSessionDict

    def timeSpentPerDay(self):
        datesDict = {}

        for session in self.userSessions:
            startDateTime = time.strftime('%Y-%m-%d', time.localtime(session.StartTime))
            timeSpent = session.EndTime - session.StartTime
            if startDateTime in datesDict:
                datesDict[startDateTime] = datesDict[startDateTime] + timeSpent
            else:
                datesDict[startDateTime] = timeSpent
        return datesDict

    def timeSpentPerProgram(self):
        userProgramsDict = {}

        for session in self.userSessions:
            sessionAnalysis = SessionAnalysis(session.key)
            perSessionProgs = sessionAnalysis.sessionTimeSpentPerProgram()
            progs = perSessionProgs.keys()

            for program in progs:
                if program in userProgramsDict:
                    userProgramsDict[program] = userProgramsDict[program] + perSessionProgs[program]
                else:
                    userProgramsDict[program] = perSessionProgs[program]

        return userProgramsDict

    def numberOfKeystrokesPerSession(self):
        keystrokesPerSessionDict = {}

        for session in self.userSessions:
            sessionAnalysis = SessionAnalysis(session.key)
            keystrokes = sessionAnalysis.sessionTotalKeyPress()
            startDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session.StartTime))
            keystrokesPerSessionDict[startDateTime] = keystrokes

        return keystrokesPerSessionDict

    def numberOfActionsPerSession(self):
        actionsPerSessionDict = {}

        for session in self.userSessions:
            sessionAnalysis = SessionAnalysis(session.key)
            actions = sessionAnalysis.sessionTotalActions()
            startDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session.StartTime))
            actionsPerSessionDict[startDateTime] = actions

        return actionsPerSessionDict

    def numberOfClicksPerSession(self):
        clicksPerSessionDict = {}

        for session in self.userSessions:
            sessionAnalysis = SessionAnalysis(session.key)
            clicks = sessionAnalysis.sessionTotalMouseClicks()
            startDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session.StartTime))
            clicksPerSessionDict[startDateTime] = clicks

        return clicksPerSessionDict

    def numberOfProgramsUsedPerSession(self):
        programsUsedPerSessionDict = {}

        for session in self.userSessions:
            sessionAnalysis = SessionAnalysis(session.key)
            perSessionProgs = sessionAnalysis.sessionListOfPrograms()
            startDateTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session.StartTime))
            programsUsedPerSessionDict[startDateTime] = len(perSessionProgs)

        return programsUsedPerSessionDict
