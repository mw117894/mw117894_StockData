import os
from urllib.request import urlopen

local_path_GOOG = os.path.join('data', 'GOOG.csv')
local_path_IBM = os.path.join('data', 'IBM.csv')
local_path_MSFT = os.path.join('data', 'MSFT.csv')

GOOG_url = "https://query1.finance.yahoo.com/v7/finance/download/GOOG?period1=1606860742&period2=1638396742&interval=1d&events=history&includeAdjustedClose=true"
IBM_url = "https://query1.finance.yahoo.com/v7/finance/download/IBM?period1=1606860899&period2=1638396899&interval=1d&events=history&includeAdjustedClose=true"
MSFT_url = "https://query1.finance.yahoo.com/v7/finance/download/MSFT?period1=1606860932&period2=1638396932&interval=1d&events=history&includeAdjustedClose=true"

paths = {local_path_GOOG: GOOG_url, local_path_IBM: IBM_url, local_path_MSFT: MSFT_url}

if not (os.path.isdir('data')):
    print('There is no "data" directory. Creating...')
    os.mkdir('data')

for path in paths.keys():

    if not os.path.isfile(path):
        url = paths[path]
        print("No file found under {} path. Downloading from {}...".format(path, url))
        with urlopen(url) as file, open(path, 'wb') as f:
            f.write(file.read())
    else:
        print("File {} is already downloaded".format(path))

for filename in os.listdir("data"):

    if filename.endswith('csv') and not filename.startswith("OUT"):
        print("Reading {} file...".format(filename))

        with open(os.path.join('data', filename), "r") as file:
            rows =[]

            for line in file.readlines():
                line = line.replace("\n","")
                rows.append(line.split(","))

        print("Adding Close/Open percentage difference...")
        openIndex = rows[0].index('Open')
        closeIndex = rows[0].index('Close')

        for row in rows:
            if rows.index(row) == 0:
                row.append('Close/Open difference...')
            else:
                difference = (float(row[closeIndex])-float(row[openIndex]))/float(row[openIndex])
                row.append(difference)

        newFileName = "OUT_"+filename
        newFileContent = ""

        for row in rows:
            for element in row:
                if row.index(element) < len(row)-1:
                    newFileContent +=element.__str__() + ","
                else:
                    newFileContent += element.__str__() + "\n"

        print("Saving new file under {} path.".format(os.path.join('data',newFileName)))

        with open(os.path.join('data',newFileName),"w") as newFile:
            newFile.write(newFileContent)

        print("Success!\n")