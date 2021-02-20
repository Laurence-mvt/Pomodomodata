# pomo.py - Pomodomodata: a super-simple, textual pomodoro app that records usage data to enable time tracking

import time, datetime
import openpyxl
import pyinputplus as pyip 

pomsComplete = 0 # number of pomodoros completed
currentPom = 0 # number of the current pomodoro

input('Ciao, world! Welcome to Pomodomodata, a pomodoro app. Press enter to begin first pomodoro.')
counting = True
while counting == True:
    currentPom += 1
    pomStartTime = datetime.datetime.now()
    print(f"Pom start time: {pomStartTime.strftime('%a, %d %b %Y: %H:%M:%S')}")
    # after 25 minutes
    while datetime.datetime.now() - pomStartTime < datetime.timedelta(minutes=0, seconds=3):
        time.sleep(1)
        # if counting set to False (i.e user indication to skip or quit, break this while loop    
        # if user wants to pause, ask for user input and resume counting when they input to resume
    # if user wants to quit, break outer while loop
    pomsComplete += 1
    print(f'Poms completed: {pomsComplete}')
    pomEndTime = datetime.datetime.now()
    print(f"Pom complete - {pomEndTime.strftime('%a, %d %b %Y: %H:%M:%S')} - 5 minute break")
    while datetime.datetime.now() - pomEndTime < datetime.timedelta(minutes=0, seconds=3):
        time.sleep(1)
"""        try: # need to fix this - need better method to quit, pause and skip - try threading, one thread to watch for user commands
            quitSkip = pyip.inputMenu(choices=['Quit', 'Skip break'], prompt='Say now if you would like to quit or skip break', timeout=3, numbered=True)
            if quitSkip == 'Quit':
                counting = False
            elif quitSkip == 'Skip':
                break
        except TimeoutError:
            break"""    

print('END OF PROGRAM')
