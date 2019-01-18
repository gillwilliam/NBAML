import csv
import os
from operator import itemgetter

print(os.getcwd())

#categories = ["Year", "Player", "Pos", "GP", "MP", "FGM", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "OREB", "DREB", "TRB", "AST", "STL", "BLK", "TOV", "PTS"]
categories_num = [1,2,3,6,8,31,32,33,34,35,36,41,42,43,44,45,46,47,48,49,50,52]

mvps = dict()
mvps['2017'] = 'Russell Westbrook'
mvps['2016'] = 'Stephen Curry'
mvps['2015'] = 'Stephen Curry'
mvps['2014'] = 'Kevin Durant'
mvps['2013'] = 'LeBron James'
mvps['2012'] = 'LeBron James'
mvps['2011'] = 'Derrick Rose'
mvps['2010'] = 'LeBron James'
mvps['2009'] = 'LeBron James'
mvps['2008'] = 'Kobe Bryant'

years = mvps.keys()
mvp_players = mvps.values()

data_to_write = list()
with open('Seasons_Stats.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            #print("{}".format(", ".join(row)))
            #print(", ".join(itemgetter(*categories_num)(row)))
            data_to_write.append([*itemgetter(*categories_num)(row)] + ['MVP'])
            print(data_to_write[0])
            line_count += 1
        else:
            if row[1] in years:

                if mvps[row[1]] == row[2]:
                    data_to_write.append([*itemgetter(*categories_num)(row)] + ['0'])
                else:
                    data_to_write.append([*itemgetter(*categories_num)(row)] + ['1'])

with open('player_data_mvp.csv', mode='w') as mvp_file:
    mvp_writer = csv.writer(mvp_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for row in data_to_write:
        mvp_writer.writerow(row)
