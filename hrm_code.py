import csv

time = []
voltage = []

with open('file.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        time.append(row[0])
        voltage.append(row[1])

print(time)
print(voltage)
