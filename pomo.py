# pomo.py - Pomodomodata: a super-simple, textual pomodoro app that records usage data to enable time tracking

import time, datetime, sys, csv, os, pprint
from pathlib import Path
import simpleaudio
from previousSessionSettings import prevPomSettings
import pyinputplus as pyip

# TODO: check if run in default mode with the below default settings, eg. -d in command line
#  default settings
focusTime = 25
normalBreakTime = 5
longBreakTime = 25
testFocusTime = 0
testNormalBreakTime = 0
testLongBreakTime = 0
pomsToLongBreak = 6 # number of poms between long breaks is 6 by default
pomTarget = None # target number of pomodors for the day
pomsCompleteToday = 0 # total complete on day program runs, including previous sessions that day

# get previous sessions settings if no settings given in command line and not run in default mode
focusTime = prevPomSettings['focusTime']
normalBreakTime = prevPomSettings['normalBreakTime']
longBreakTime = prevPomSettings['longBreakTime']
pomsToLongBreak = prevPomSettings['pomsToLongBreak']
pomTarget = prevPomSettings['pomTarget']
sessionDate = prevPomSettings['date']
pomsCompleteToday = prevPomSettings['pomsCompleteToday']
# if previous session was on an earlier date, reset pomsCompleteToday
if sessionDate != str(datetime.datetime.today().strftime('%Y-%m-%d')):
    pomsCompleteToday = 0

# add an options mode, -o, where user can respond to prompts to enter settings
if '-o' in sys.argv:
    print('Enter your preferred settings (focus and break times in minutes)')
    focusTime = pyip.inputInt(prompt="Focus time: ", min=1)
    normalBreakTime = pyip.inputInt(prompt="Regular break time: ", min=1)
    longBreakTime = pyip.inputInt(prompt="Long break time: ", min=1)
    pomsToLongBreak = pyip.inputInt(prompt="Sessions to long break: ", min=1)
    pomTarget = pyip.inputInt(prompt="Enter target number of poms (leave blank for no target): ", min=1, blank=True)
    if pomTarget == '':
        pomTarget = None

if pomTarget != None:
    pomsTilTarget = pomTarget - pomsCompleteToday


#TODO check if any settings specified in the command line, eg for focus/break times
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
        print(f"Pom start time: {pomStartTime.strftime('%a, %d %b %Y: %H:%M:%S')}  ".ljust(40, '.') +  f"  Focus until: {(pomStartTime + datetime.timedelta(minutes=focusTime, seconds=testFocusTime)).strftime('%H:%M:%S')}".rjust(40, '.'))
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
    # update previous session settings
    with open('previousSessionSettings.py', 'w') as settingsFileObj:
        settingsFileObj.write('prevPomSettings = ' + pprint.pformat(currentPomSettings))

    sys.exit(f"\nGood job! See you soon.")

# save pom sessions data 
with open('myPomoData.csv', 'a') as pomDataCSV:
    pomDictWriter = csv.DictWriter(pomDataCSV, fieldnames=['pomSession','pomStartDatetime', 'pomEndDatetime', 'focus', 'tired', 'mood', 'comment'])
    for pom in dataBuffer:
        pomDictWriter.writerow(pom)

# update previous session settings
with open('previousSessionSettings.py', 'w') as settingsFileObj:
    settingsFileObj.write('prevPomSettings = ' + pprint.pformat(currentPomSettings))


print('Good job! See you soon.')