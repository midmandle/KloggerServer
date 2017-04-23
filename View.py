import string
from SessionAnalysis import *
from UserAnalysis import *
from PopulationAnalysis import *
import json

def returnViewOverviewAndTimeline(sessionKey):
    sessionAnalysis = SessionAnalysis(sessionKey)

    output = {}
    overview = {}

    output["Timeline"] = sessionAnalysis.sessionTimeline()
    output["Time_Spent_Per_Program"] = sessionAnalysis.sessionTimeSpentPerProgram()
    output["List_Of_Programs_In_Session"] = sessionAnalysis.sessionListOfPrograms()
    output["Actions_Per_Program"] = sessionAnalysis.sessionActionsPerProgram()
    output["Keypresses_Per_Program"] = sessionAnalysis.sessionKeypressesPerProgram()
    output["Mouseclicks_Per_Program"] = sessionAnalysis.sessionMouseClicksPerProgram()

    overview["Total_Number_Of_Actions"] = sessionAnalysis.sessionTotalActions()
    overview["Total_Keypresses"] = sessionAnalysis.sessionTotalKeyPress()
    overview["Total_Mouse_Clicks"] = sessionAnalysis.sessionTotalMouseClicks()
    overview["Total_Time_In_Session"] = sessionAnalysis.sessionTotalTimeSpentSession()

    output["Overview"] = overview

    return json.dumps(output)

def returnViewUserData(userID):
    userAnalysis = UserAnalysis(userID)

    userData = {}

    userData["Time_Spent_Per_Session"] = userAnalysis.timeSpentPerSession()
    userData["Time_Spent_Per_Day"] = userAnalysis.timeSpentPerDay()
    userData["Time_Spent_Per_Program"] = userAnalysis.timeSpentPerProgram()
    userData["Number_Of_Keys_Per_Session"] = userAnalysis.numberOfKeystrokesPerSession()
    userData["Number_Of_Actions_Per_Session"] = userAnalysis.numberOfActionsPerSession()
    userData["Number_Of_Click_Per_Session"] = userAnalysis.numberOfClicksPerSession()
    userData["Number_Of_Programs_User_Per_Session"] = userAnalysis.numberOfProgramsUsedPerSession()


    return json.dumps(userData);

def returnViewPopulationData(populationIDs):
    popAnalysis = PopulationAnalysis(populationIDs)

    populationData = {}

    populationData["Average_Time_Per_Session"] = popAnalysis.populationAverageTimePerSession()
    populationData["Average_Time_Per_Day"] = popAnalysis.populationAverageTimePerDay()
    populationData["Average_Actions_Per_Session"] = popAnalysis.populationAverageActionsPerSession()
    populationData["Average_Keys_Per_Session"] = popAnalysis.populationAverageKeyPressPerSession()
    populationData["Average_Click_Per_Session"] = popAnalysis.populationAverageMouseClickPerSession()
    populationData["Average_Number_Programs_Per_Session"] = popAnalysis.populationAverageNumProgramsPerSession()

    return json.dumps(populationData)
