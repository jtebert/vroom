
import csv
import sys, getopt


def applyObsLabel(csvfile, label):

    #read in the file
    rows = []
    endRows = []

    with open(csvfile, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            rowList = []
            for column in row:
                rowList.append(int(column))
            rows.append(rowList)
                           

    #edit contents with label
    for row in rows:
        endRow = []
        for val in row:
            newVal = "[{0},{1}]".format(int(val),str(label))
            endRow.append(newVal)
        endRows.append(endRow)

    #save back into the file
    with open(csvfile, 'w') as csvFile:
        writer = csv.writer(csvFile)
        for row in endRows:
            print row
            writer.writerow(row)

if __name__ == "__main__":
    
    try: 
        opts,args = getopt.getopt(sys.argv[2:],"l:")
    except getopt.GetoptError:
        print "editSample.py samplePath -l 'labelName'"
        sys.exit(2)

    samplePath = sys.argv[1]
    print samplePath

    for opt,arg in opts:
        if opt == '-l':
            label = arg
            applyObsLabel(samplePath, label)
    
    
