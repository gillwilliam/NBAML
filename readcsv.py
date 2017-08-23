import csv
import sys
import requests
import json

x_1 = []
x_2 = []

combined = []
index = 0
f = open('freeagents2016.csv', 'rt')
try:
    reader = csv.reader(f)
    for row in reader:
        if(index > 0):
            if(len(row[1]) > 0 and row[1][0] == 'S' and len(row[1].split(" ")[1].split("-yr/")) == 2):
                x_1.append(row[0])
                a = row[1].split(" ")[1].split("-yr/")
                years = a[0]
                amount = a[1].split("$")[1].split("M")[0]
                if(amount[len(amount) - 1] == 'K'):
                    amount = amount.split('K')[0]
                x_2.append(float(amount)/float(years))
                temp = [row[0], float(amount)/float(years)]
                combined.append(temp)
        index+=1
finally:
    f.close()

print(x_1[0])
print(x_2[0])

players = requests.get('http://localhost:8080/api/leagueleaders/allplayers').json()["test"]

playerWithSal = []
for player in players:
    playerName = player["PLAYER"]
    for playerSal in combined:
        if(playerSal[0] == playerName):
            a = player
            a['Salary'] = playerSal[1]
            playerWithSal.append(a)



print(playerWithSal[0])
