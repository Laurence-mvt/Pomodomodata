# pomo.py - Pomodomodata: a super-simple, textual pomodoro app that records usage data to enable time tracking

import time, datetime, sys
import pyinputplus as pyip 

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

pomsComplete = 0 # number of pomodoros completed
currentPom = 0 # number of the current pomodoro

# start program
input('Ciao, world! Welcome to Pomodomodata, a pomodoro app. Press enter to begin first pomodoro.')
counting = True

while counting == True:
    currentPom += 1
    pomStartTime = datetime.datetime.now()
    print(f"Pom start time: {pomStartTime.strftime('%a, %d %b %Y: %H:%M:%S')}")

    # after 25 minutes
    while datetime.datetime.now() - pomStartTime < datetime.timedelta(minutes=focusTime, seconds=testFocusTime):
        time.sleep(1)
    # pom session complete
    pomsComplete += 1
    print(f'Poms completed: {pomsComplete}')
    pomEndTime = datetime.datetime.now()
    print(f"Pom complete - {pomEndTime.strftime('%a, %d %b %Y: %H:%M:%S')} - 5 minute break until {(pomEndTime + datetime.timedelta(minutes=focusTime, seconds=testFocusTime)).strftime('%H:%M:%S')}")

    # get user reflection on session and choice to continue or quit
    userInput = ''
    while len(userInput.split(' ')) < 3:
        print('enter q to quit (optional) and ### for focus, tired and mood levels (1-5) and comment on your pom session, eg. "554 completed report plan"')
        userInput = input('[q] ### comment:  ')
    # if user wants to quit, end the pomodoro loop
    if userInput[0] == 'q':
        break
    # otherwise, continue and check if break time over:
    if datetime.datetime.now() - pomEndTime < datetime.timedelta(minutes=breakTime, seconds=testBreakTime):
        # break time not over
        while datetime.datetime.now() - pomEndTime < datetime.timedelta(minutes=breakTime, seconds=testBreakTime):
            time.sleep(1)
    # else break time over and start next pomm session

print('END OF PROGRAM')