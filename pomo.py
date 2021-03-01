# pomo.py - Pomodomodata: a textual pomodoro app that records usage data to enable time tracking

import time, datetime, sys, csv, os
from pathlib import Path
import simpleaudio
import pyinputplus as pyip
import shelve

def setSettings():
    # gets settings from user input function
    print('Enter your preferred settings (focus and break times in minutes)')
    focusTime = pyip.inputInt(prompt="Focus time: ", min=1)
    normalBreakTime = pyip.inputInt(prompt="Regular break time: ", min=1)
    longBreakTime = pyip.inputInt(prompt="Long break time: ", min=1)
    pomsToLongBreak = pyip.inputInt(prompt="Sessions to long break: ", min=1)
    pomTarget = pyip.inputInt(prompt="Enter target number of poms (leave blank for no target): ", min=1, blank=True)
    if pomTarget == '':
        pomTarget = None
    return focusTime, normalBreakTime, longBreakTime, pomsToLongBreak, pomTarget

firstTime = False

#  initial settings
focusTime = 25
normalBreakTime = 5
longBreakTime = 25
testFocusTime = 0
testNormalBreakTime = 0
testLongBreakTime = 0
pomsToLongBreak = 6 # number of poms between long breaks is 6 by default
pomTarget = None # target number of pomodors for the day
pomsCompleteToday = 0 # total complete on day program runs, including previous sessions that day

# check if run in default mode with the below default settings, eg. -d in command line
if '-d' in sys.argv:
    #  default settings
    try:
        with shelve.open('pomSettings') as db:
            focusTime = db['defaultSettings']['focusTime']
            normalBreakTime = db['defaultSettings']['normalBreakTime']
            longBreakTime = db['defaultSettings']['longBreakTime']
            pomsToLongBreak = db['defaultSettings']['pomsToLongBreak']
            pomTarget = db['defaultSettings']['pomTarget']
    except KeyError:
        firstTime = True
# otherwise,get previous sessions settings and info if no settings given in command line and not run in default mode
else:
    try:
        with shelve.open('pomSettings') as db:
            focusTime = db['prevPomSettings']['focusTime']
            normalBreakTime = db['prevPomSettings']['normalBreakTime']
            longBreakTime = db['prevPomSettings']['longBreakTime']
            pomsToLongBreak = db['prevPomSettings']['pomsToLongBreak']
            pomTarget = db['prevPomSettings']['pomTarget']
            prevSessionDate = db['prevPomSettings']['date']
            pomsCompleteToday = db['prevPomSettings']['pomsCompleteToday']
            # if previous session was on an earlier date, reset pomsCompleteToday
            if prevSessionDate != str(datetime.datetime.today().strftime('%Y-%m-%d')):
                pomsCompleteToday = 0
    except KeyError:
        firstTime = True

# if the very first time, use inital settings and set defaults
if firstTime: 
    sys.argv.append('-c') # add -c to sys.argv to run configurations if run for first time
    with shelve.open('pomSettings') as db:
        defaultSettings = {'focusTime': focusTime,
                            'normalBreakTime': normalBreakTime,
                            'longBreakTime': longBreakTime,
                            'pomsToLongBreak': pomsToLongBreak,
                            'pomTarget': pomTarget}
        db['defaultSettings'] = defaultSettings

# if run in configurations mode, -c, user can update the default settings and enter focus themes, eg. coding, mathClass, homework, work
if '-c' in sys.argv:
    defaultSettings = {} # TODO only ask update what if not first time
    updateWhat = ''
    if not firstTime:
        updateWhat = pyip.inputMenu(['Default settings', 'Focus areas', 'Both'], prompt="What would you like to update? \n", numbered=True)
    if updateWhat.lower() == 'default settings':
        focusTime, normalBreakTime, longBreakTime, pomsToLongBreak, pomTarget = setSettings()
        # update default settings with shelve
        defaultSettings = {'focusTime': focusTime,
                            'normalBreakTime': normalBreakTime,
                            'longBreakTime': longBreakTime,
                            'pomsToLongBreak': pomsToLongBreak,
                            'pomTarget': pomTarget}
        with shelve.open('pomSettings') as db:
            db['defaultSettings'] = defaultSettings
    elif updateWhat.lower() == 'focus areas':
        correct = ''    
        with shelve.open('pomSettings') as db:
            try: # try in case of first time running or no focus areas existing yet
                while correct not in ['y', 'yes']:
                    focusAreas = db['focusAreas']
                    resultFocusAreas = list(focusAreas)
                    print(f"You're current focus themes are {', '.join(resultFocusAreas)}")
                    stringUpdateFocusAreas = input('Enter additional focus themes to add, and enter existing themes to remove, separated by commas:\n')
                    listUpdateFocusAreas = stringUpdateFocusAreas.split(', ')
                    for area in listUpdateFocusAreas:
                        if area in resultFocusAreas:
                            resultFocusAreas.remove(area)
                        else:
                            resultFocusAreas.append(area)
                    while True:
                        correct = input(f"Your new focus themes will be: {', '.join(resultFocusAreas)}\nIs that correct?  ").lower()
                        if correct in ['y', 'yes', 'n', 'no']:
                            break
                        else:
                            print('please enter y or yes or n or no')
                db['focusAreas'] = resultFocusAreas
            except KeyError: # if no focus areas exist yet
                while correct not in ['y', 'yes']:
                    stringUpdateFocusAreas = input('Enter additional focus themes to add, and enter existing themes to remove, separated by commas:\n')
                    listUpdateFocusAreas = stringUpdateFocusAreas.split(', ')
                    resultFocusAreas = listUpdateFocusAreas
                    while True:
                        correct = input(f"Your new focus themes will be: {', '.join(resultFocusAreas)}\nIs that correct?  ").lower()
                        if correct in ['y', 'yes', 'n', 'no']:
                            break
                        else:
                            print('please enter y or yes or n or no')
                db['focusAreas'] = resultFocusAreas
    else: # if update both selected, or it is the first time 
        focusTime, normalBreakTime, longBreakTime, pomsToLongBreak, pomTarget = setSettings()
        defaultSettings = {'focusTime': focusTime,
                            'normalBreakTime': normalBreakTime,
                            'longBreakTime': longBreakTime,
                            'pomsToLongBreak': pomsToLongBreak,
                            'pomTarget': pomTarget}
        print('\n')
        # update both with shelve
        with shelve.open('pomSettings') as db:
            db['defaultSettings'] = defaultSettings
            correct = '' 
            try: # try in case of first time running or no focus areas existing yet
                while correct not in ['y', 'yes']:
                    focusAreas = db['focusAreas']
                    resultFocusAreas = list(focusAreas)
                    print(f"You're current focus themes are {', '.join(resultFocusAreas)}")
                    if firstTime:
                        prompt = 'Enter focus themes, separated by commas:\n'
                    else:
                        prompt = 'Enter additional focus themes to add, and enter existing themes to remove, separated by commas:\n'
                    stringUpdateFocusAreas = input(prompt)
                    listUpdateFocusAreas = stringUpdateFocusAreas.split(', ')
                    for area in listUpdateFocusAreas:
                        if area in resultFocusAreas:
                            resultFocusAreas.remove(area)
                        else:
                            resultFocusAreas.append(area)
                    while True:
                        correct = input(f"Your new focus themes will be: {', '.join(resultFocusAreas)}\nIs that correct?  ").lower()
                        if correct in ['y', 'yes', 'n', 'no']:
                            break
                        else:
                            print('please enter y or yes or n or no')
                db['focusAreas'] = resultFocusAreas
            except KeyError: # if no focus areas exist yet
                while correct not in ['y', 'yes']:
                    stringUpdateFocusAreas = input('Enter additional focus themes to add, and enter existing themes to remove, separated by commas:\n')
                    listUpdateFocusAreas = stringUpdateFocusAreas.split(', ')
                    resultFocusAreas = listUpdateFocusAreas
                    while True:
                        correct = input(f"Your new focus themes will be: {', '.join(resultFocusAreas)}\nIs that correct?  ").lower()
                        if correct in ['y', 'yes', 'n', 'no']:
                            break
                        else:
                            print('please enter y or yes or n or no')
                db['focusAreas'] = resultFocusAreas
    

# TODO consider when/whether to ask this: focusArea = pyip.inputMenu(focusAreas, prompt="What are you working on today?", numbered=True)
# focusArea = ''

# if run in options mode, -o, user can respond to prompts to enter settings
if '-o' in sys.argv:
    focusTime, normalBreakTime, longBreakTime, pomsToLongBreak, pomTarget = setSettings()
    focusArea = pyip.inputMenu(focusAreas, prompt="What are you working on today?", numbered=True)

if pomTarget != None:
    pomsTilTarget = pomTarget - pomsCompleteToday


#TODO check if any settings specified in the command line, eg for focus/break times, and update shelf if needed
if len(sys.argv) > 1:
    if sys.argv[1].isdecimal():
        pomsToLongBreak = int(sys.argv[1])
    if len(sys.argv) > 2:
        if sys.argv[2].isdecimal():
            pomTarget = sys.argv[2]
# TODO update saved settings if any given
currentPomSettings = {
    'focusTime': focusTime,
    'normalBreakTime': normalBreakTime,
    'longBreakTime': longBreakTime,
    'pomsToLongBreak': pomsToLongBreak,
    'pomTarget': pomTarget,
    'date': str(datetime.datetime.today().strftime('%Y-%m-%d')),
    'pomsCompleteToday': pomsCompleteToday
}

# check if run in test mode for short focus and break sessions for convenient testing
testMode = False
if 'test' in sys.argv:
    testMode = True

# if run in test mode, set focus time as 2 seconds, break time as 5 seconds
if testMode:
    focusTime = 0
    normalBreakTime = 0
    longBreakTime = 0
    testFocusTime = 2
    testNormalBreakTime = 5
    testLongBreakTime = 10

# get notification sound
sound = os.listdir('useEndSound')[0]
soundPath = str(Path('useEndSound')/sound)
wave_obj = simpleaudio.WaveObject.from_wave_file(soundPath)

# motivational messages
motivations = ['Forza!', 'Ce la fai!', 'Coraggio!']

# if the first time running the program, create a new csv with headers to store data
p = Path('myPomoData.csv')
# if first time using program and no prevous csv file 
if not p.exists():
    pomDataCSV = open('myPomoData.csv', 'w')
    pomDataWriter = csv.writer(pomDataCSV)
    # add headers to csv
    pomDataWriter.writerow(['pomSession','pomStartDatetime', 'pomEndDatetime', 'focus', 'tired', 'mood', 'comment'])
    pomDataCSV.close()

currentPom = 0 # number of the current pomodoro
sessionPomsComplete = 0 # number of poms complete in current session

# create list of dictionary to store the sessions data
dataBuffer = []
# currentPomData = {'pomNumber': the number of that pomodoro for the current program session,
#               'pomStartDatetime': start time of pom session, 
#               'pomEndDatetime': end time of pom session,
#               'focus': 1-5 rating of how focused user was (5 highest),
#               'tired': 1-5 rating of how tired user was (5 highest),
#               'mood': 1-5 rating of how cheerful/happy/content user was (5 highest),
#               'comment': what user did, how they felt, any observation}

# start up display
print(f'\n')
print('  PomodomoData  '.center(80, '_'))
print(f'\n')
print(f'Ciao, world! Welcome to PomodomoData, a Pomodoro app.\n'.ljust(80, ' '))
print('------'.center(85, ' ') + '\n')
print(f'PomodomoData allows you to track your productivity, focus, tiredness, and mood levels.\n'.ljust(80))
print(f'''After each focus session enter: q to quit or s to skip break (optional)
... ### for focus, tired and mood levels (1-5)...
... and a comment on your pom session (optional).

For example, "554 completed report plan" or, "q 353 time for bed".

Press ctrl-C to save your progress and quit the app at any time.\n''')
print('------'.center(80, ' ') + '\n')

# -------------------POMODOROS START HERE ON USER INPUT----------------
# start pomodoros on user input
input('Press enter to begin first pomodoro.')
try:
    while True:
        currentPom += 1
        pomStartTime = datetime.datetime.now()
        currentPomData={'pomSession':currentPom}
        currentPomData['pomStartDatetime'] = pomStartTime.strftime('%Y-%m-%d %H:%M:%S')
        print(f"Pom start time: {pomStartTime.strftime('%a, %d %b %Y: %H:%M:%S')}  ".ljust(44, '.') +  f"  Focus until: {(pomStartTime + datetime.timedelta(minutes=focusTime, seconds=testFocusTime)).strftime('%H:%M:%S')}".rjust(36, '.'))
        print(f'Current pom: {currentPom}\n')
        
        # set break time depending on if long break or regular
        if currentPom % pomsToLongBreak == 0:
            breakTime = longBreakTime
            testBreakTime = testLongBreakTime
        else:
            breakTime = normalBreakTime
            testBreakTime = testNormalBreakTime

        # after 25 minutes
        while datetime.datetime.now() - pomStartTime < datetime.timedelta(minutes=focusTime, seconds=testFocusTime):
            time.sleep(1)
        # pom session complete, play notification sound
        wave_obj.play()
        sessionPomsComplete += 1
        pomsCompleteToday += 1
        currentPomSettings['pomsCompleteToday'] = pomsCompleteToday
        if pomTarget != None:
            pomsTilTarget -= 1

        pomEndTime = datetime.datetime.now()
        currentPomData['pomEndDatetime'] = pomEndTime.strftime('%Y-%m-%d %H:%M:%S')
        print(f"Pom #{sessionPomsComplete} complete - {pomEndTime.strftime('%a, %d %b %Y: %H:%M:%S')} - {breakTime} minute break until {(pomEndTime + datetime.timedelta(minutes=breakTime, seconds=testBreakTime)).strftime('%H:%M:%S')}")
        # update on progress towards pom target, if halfway, or closer to target
        if pomTarget != None:
            if pomTarget / pomsCompleteToday == 2:
                print(f"You're halfway to your goal of {pomTarget} poms - Non mollare!")
            elif 0 < pomsTilTarget <= 3:
                print(f"You're only {pomsTilTarget} poms away from your goal today - {motivations[pomsTilTarget -1]}")
            elif pomTarget == pomsCompleteToday:
                print(f'Goal of {pomTarget} poms achieved - Bravissimo!')
        # get user reflection on session and choice to continue or quit
        userInput = ''
        while len(userInput.split(' ')) < 1 or userInput == '': 
            userInput = input('Enter [q,s] ### [comment]:  ')

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
        else:
            sessionRating = userInput[0]
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
        # else break time over, play notification sound and start next pomm session
        wave_obj.play()

# if user interupts to quit, save data before quitting
except KeyboardInterrupt:
    with open('myPomoData.csv', 'a') as pomDataCSV:
        pomDictWriter = csv.DictWriter(pomDataCSV, fieldnames=['pomSession','pomStartDatetime', 'pomEndDatetime', 'focus', 'tired', 'mood', 'comment'])
        for pom in dataBuffer:
            pomDictWriter.writerow(pom)
    # update previous session settings - MOVE SYS.EXIT BELOW
    with shelve.open('pomSettings') as db:
        prevPomSettings = currentPomSettings
        db['prevPomSettings'] = prevPomSettings
    sys.exit(f"\nGood job! See you soon.")

# save pom sessions data 
with open('myPomoData.csv', 'a') as pomDataCSV:
    pomDictWriter = csv.DictWriter(pomDataCSV, fieldnames=['pomSession','pomStartDatetime', 'pomEndDatetime', 'focus', 'tired', 'mood', 'comment'])
    for pom in dataBuffer:
        pomDictWriter.writerow(pom)

# update previous session settings
with shelve.open('pomSettings') as db:
        prevPomSettings = currentPomSettings
        db['prevPomSettings'] = prevPomSettings

print('Good job! See you soon.')