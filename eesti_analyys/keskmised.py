
import csv
import os
from statistics import mean

"""
dimensioonide hinnangute keskmiste arvutamine
"""

folder = '../dimensions_cvs'



for f in os.listdir(folder):
    filename = os.path.join(folder, f)

    if os.path.isfile(filename):
        print(filename)
        andmed = []
        with open(filename) as fid:
            csv_reader = csv.reader(fid)
            next(csv_reader)
            for line in csv_reader:
                keskmine = mean([float(skoor) for skoor in line[1:]])

                andmed.append((line[0], keskmine))

        andmed.sort(key=lambda t: t[0])
        for rida in andmed:
            print(f'{rida[0]} == {rida[1]}')
        print('============================')