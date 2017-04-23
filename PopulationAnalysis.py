from UserAnalysis import UserAnalysis
class PopulationAnalysis:
    def __init__(self, populationIDs):
        self.populationIDs = populationIDs

    def populationAverageTimePerSession(self):
        populationAverageTimeSession = {}
        for user in self.populationIDs:
            userAnalysis = UserAnalysis(user)
            userTimeSpentPerSession = userAnalysis.timeSpentPerSession()
            average = 0
            for session in userTimeSpentPerSession:
                average += userTimeSpentPerSession[session]
            average = average / len(userTimeSpentPerSession)
            populationAverageTimeSession[user] = average
        return populationAverageTimeSession

    def populationAverageTimePerDay(self):
        populationAverageTimeDay = {}
        for user in self.populationIDs:
            userAnalysis = UserAnalysis(user)
            userTimeSpentPerDay = userAnalysis.timeSpentPerDay()
            average = 0
            for session in userTimeSpentPerDay:
                average += userTimeSpentPerDay[session]
            average = average / len(userTimeSpentPerDay)
            populationAverageTimeDay[user] = average
        return populationAverageTimeDay

    def populationAverageActionsPerSession(self):
        populationAverageActionsSession = {}
        for user in self.populationIDs:
            userAnalysis = UserAnalysis(user)
            userActionsPerSession= userAnalysis.numberOfActionsPerSession()
            average = 0
            for session in userActionsPerSession:
                average += userActionsPerSession[session]
            average = average / len(userActionsPerSession)
            populationAverageActionsSession[user] = average
        return populationAverageActionsSession

    def populationAverageKeyPressPerSession(self):
        populationAverageKeyPressSession = {}
        for user in self.populationIDs:
            userAnalysis = UserAnalysis(user)
            userKeyPressPerSession= userAnalysis.numberOfKeystrokesPerSession()
            average = 0
            for session in userKeyPressPerSession:
                average += userKeyPressPerSession[session]
            average = average / len(userKeyPressPerSession)
            populationAverageKeyPressSession[user] = average
        return populationAverageKeyPressSession

    def populationAverageMouseClickPerSession(self):
        populationAverageClicksSession = {}
        for user in self.populationIDs:
            userAnalysis = UserAnalysis(user)
            userClicksPerSession= userAnalysis.numberOfClicksPerSession()
            average = 0
            for session in userClicksPerSession:
                average += userClicksPerSession[session]
            average = average / len(userClicksPerSession)
            populationAverageClicksSession[user] = average
        return populationAverageClicksSession

    def populationAverageNumProgramsPerSession(self):
        populationAverageNumberProgsSession = {}
        for user in self.populationIDs:
            userAnalysis = UserAnalysis(user)
            userNumberProgsPerSession= userAnalysis.numberOfProgramsUsedPerSession()
            average = 0
            for session in userNumberProgsPerSession:
                average += userNumberProgsPerSession[session]
            average = average / len(userNumberProgsPerSession)
            populationAverageNumberProgsSession[user] = average
        return populationAverageNumberProgsSession
