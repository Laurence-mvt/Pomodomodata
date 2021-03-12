# addCols.py - added some additional fields to the data tracking csv file

import csv
from pathlib import Path

copy = open('copyMyPomoData.csv', 'r')
copyReader = csv.DictReader(copy)

newRows = []
for index, oldRow in enumerate(list(copyReader)):
    newRows.append(oldRow)
    newRows[index]['focusArea'] = 'NA'
    newRows[index]['pomTarget'] = 'NA'

# add new fields to past pom data for focusArea and pomTarget, with NA as the entry
with open('newMyPomoData.csv', 'w') as newFile:
    newWriter = csv.DictWriter(newFile, fieldnames=['pomSession','pomStartDatetime', 'pomEndDatetime', 'focusArea', 'pomTarget', 'focus', 'tired', 'mood', 'comment'])
    newWriter.writeheader()
    for row in newRows:
        newWriter.writerow(row)
