# pomo.py - Pomodomodata: a super-simple, textual pomodoro app that records usage data to enable time tracking

import time, datetime, sys, csv, os
from pathlib import Path
import simpleaudio

# if run in test mode, set focus time as 2 seconds, break time as 5 seconds
focusTime = 25
breakTime = 5
testFocusTime = 0
testBreakTime = 0
if len(sys.argv) > 1:
    focusTime = 0
    breakTime = 0
    testFocusTime = 2
    testBreakTime = 5

# if the first time running the program, create a new csv with headers to store data
p = Path('myPomoData.csv')
# if first time using program and no prevous csv file 
if not p.exists():
    pomDataCSV = open('myPomoData.csv', 'w')
    pomDataWriter = csv.writer(pomDataCSV)
    # add headers to csv
    pomDataWriter.writerow(['pomSession','pomStartDatetime', 'pomEndDatetime', 'focus', 'tired', 'mood', 'comment'])
    pomDataCSV.close()

pomsComplete = 0 # number of pomodoros completed
currentPom = 0 # number of the current pomodoro

# create list of dictionary to store the sessions data
dataBuffer = []
# pomSession = {'pomNumber': the number of that pomodoro for the current program session,
#               'pomStartDatetime': start time of pom session, 
#               'pomEndDatetime': end time of pom session,
#               'focus': 1-5 rating of how focused user was (5 highest),
#               'tired': 1-5 rating of how tired user was (5 highest),
#               'mood': 1-5 rating of how cheerful/happy/content user was (5 highest),
#               'comment': what user did, how they felt, any observation}

# start program
input('Ciao, world! Welcome to Pomodomodata, a pomodoro app. Press enter to begin first pomodoro.')
counting = True
# get sound path
sound = os.listdir('useSound')[0]
soundPath = str(Path('useSound')/sound)

while counting == True:
    currentPom += 1
    currentPomData={'pomSession':currentPom}
    pomStartTime = datetime.datetime.now()
    currentPomData['pomStartDatetime'] = pomStartTime
    print(f"Pom start time: {pomStartTime.strftime('%a, %d %b %Y: %H:%M:%S')}")

    # after 25 minutes
    while datetime.datetime.now() - pomStartTime < datetime.timedelta(minutes=focusTime, seconds=testFocusTime):
        time.sleep(1)
    # pom session complete 
    wave_obj = simpleaudio.WaveObject.from_wave_file(soundPath)
    wave_obj.play()
    pomsComplete += 1

    print(f'Poms completed: {pomsComplete}')
    pomEndTime = datetime.datetime.now()
    currentPomData['pomEndDatetime'] = pomEndTime
    print(f"Pom complete - {pomEndTime.strftime('%a, %d %b %Y: %H:%M:%S')} - 5 minute break until {(pomEndTime + datetime.timedelta(minutes=focusTime, seconds=testFocusTime)).strftime('%H:%M:%S')}")

    # get user reflection on session and choice to continue or quit
    userInput = ''
    while len(userInput.split(' ')) < 1 or userInput == '': 
        print('enter q to quit or s to skip break (optional) and ### for focus, tired and mood levels (1-5) and comment on your pom session (optional), eg. "554 completed report plan"')
        userInput = input('[q,s] ### [comment]:  ')
    
    # for hard quit with no session ratings, enter qh
    if userInput[:2] == 'qh':
        break
    
    # split user input into q/s ### and comment
    userInput = userInput.split(' ')
    userComment = ''
    sessionRating = ''
    if len(userInput) > 1: # user likely entered a rating
        if userInput[0] in ['q', 's', 'qh']:
            sessionRating = userInput[1]
            if len(userInput) > 2: # user entered a comment
                userComment = ' '.join(userInput[2:])
        else: # rating should be first string in input
            sessionRating = userInput[0]
            userComment = ' '.join(userInput[1:])

    # get session rating if not provided or not valid
    while len(sessionRating) != 3 or not sessionRating.isdecimal() or not all(x in ['1', '2', '3', '4', '5'] for x in sessionRating):
        sessionRatingOptionalComment = input('please record focus, tired and mood levels (1-5) and optional comment: ')
        sessionRating = sessionRatingOptionalComment[:3]
        if len(sessionRatingOptionalComment) > 3:
            userComment =  sessionRatingOptionalComment[3:]
    
    # addd session Rating to pom session data
    currentPomData.update({'focus': sessionRating[0], 'tired': sessionRating[1], 'mood': sessionRating[2]})
    currentPomData['comment'] = userComment

    # add current pom data to data buffer
    dataBuffer.append(currentPomData)

    # if user wants to quit, end the pomodoro loop
    if userInput[0] == 'q':
        break

    # if user wants to skip break, start next pomodoro
    if userInput[0] == 's':
        continue    
    
    # otherwise, check if break time over:
    if datetime.datetime.now() - pomEndTime < datetime.timedelta(minutes=breakTime, seconds=testBreakTime):
        # break time not over
        while datetime.datetime.now() - pomEndTime < datetime.timedelta(minutes=breakTime, seconds=testBreakTime):
            time.sleep(1)
    # else break time over and start next pomm session

# save pom sessions data 
with open('myPomoData.csv', 'a') as pomDataCSV:
    pomDictWriter = csv.DictWriter(pomDataCSV, fieldnames=['pomSession','pomStartDatetime', 'pomEndDatetime', 'focus', 'tired', 'mood', 'comment'])
    for pom in dataBuffer:
        pomDictWriter.writerow(pom)


print('END OF PROGRAM')