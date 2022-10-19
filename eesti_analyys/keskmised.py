
import csv
import os
from statistics import mean

"""
dimensioonide hinnangute keskmiste arvutamine
"""

folder = '~/dimensions_cvs'

andmed = []

for f in os.listdir(folder):
    filename = os.path.join(folder, f)

    if os.path.isfile(filename):
        with open(filename) as fid:

            csv_reader = csv.reader(fid)
            next(csv_reader)
            for line in csv_reader:
                keskmine = mean([float(skoor) for skoor in line[1:]])
                andmed.append([line[0], keskmine])
                print(f'{line[0]}; {keskmine}')

        print('============================')