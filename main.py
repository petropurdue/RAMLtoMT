# Imports
import os
import re
import csv

#Class Name: MAPI (mapping API)
#Role: Contain all relevant API data in one convenient object!
class MAPI:
    def __init__(self):
        self.reqResp = ""
        self.JSO = ""
        self.fieldName = ""
        self.type = ""
        self.len = ""
        self.apiPat = ""
        self.required = ""
        self.default = ""
        self.example = ""
        self.description = ""

    #Name: dispMAPI
    #Role: print all field names and values
    def dispMAPI(self):
        print(self.fieldName + ":"),
        print(vars(self))

    #Name: setFN
    #Role: Set Field Name by refining the input string to its simplest form.
    def setFN(self, inputString):
        self.fieldName = refine(inputString)

    #Name: parseData
    #Role: As refined data is inputted, sort it into the appropriate field. If it doesn't exist, state so.
    #Input:
    #   inputString: a string of data that will be parsed
    def parseData(self, inputArr):
        success = False

        what = inputArr[0]
        val = inputArr[1]

        if what == "type":
            self.type = val
            success = True
        if what == "required":
            self.required = val
            success = True
        if what == "default":
            self.default = val
            success = True
        if what == "example":
            self.example = val
            success = True
        if what == "description":
            self.description = val
            success = True
        if success == False:
            print("VALUE COULD NOT BE STORED!")
            print("##########################")
            print("#" + what + val)
            print("##########################")


#Name: getIndent
#Role: get indentation level within the file by counting the number of spaces. Used to detect child/parent dependencies
#Input:
#   inputString- a string that needs to have its spaces counted
#Return:
#   wordSpaces - an int of how many spaces are before the actual word itself
def getIndent(inputString):
    wordSpaces = 0
    for xletter in inputString:
        if xletter == " ":
            wordSpaces += 1
        else:
            break
    return wordSpaces

#Name: testFile
#Role: print file to confirm its contents
#Input:
#   FN- filename as string
#Return:
#   void
def testFile(FN):
    fptr = open(FN, "r")

    for readline in fptr:
        print(readline)

#Name: splitCol
#Role: split an input string into before and after the colon. Col is normally column, but here it means colon.
#       I like to live dangerously.
#Input:
#   inputString- a string (presumably with a colon in it)
#Return:
#   retArr- an array of two values: those before and those after the colon. The colon is not included in either half.
#TODO: Confirm it works with no colon
def splitCol(inputString):
    retArr = []
    retArr.append(refine(inputString[0:inputString.find(":")]))
    retArr.append(refine(inputString[inputString.find(":") + 1::]))
    return retArr

#Name: refine
#Role: refine a string to remove any unecessary spaces or colons. Why? Because at some point I needed that to be done.
#       don't question my methods!! (Unless you can improve them, in which case please do!)
#Input:
#   inputString- a string of the string that needs to be refined
#Return:
#   newString- the happier, cleaner string :)
def refine(inputString):
    # Refines a string to be happy :)
    newString = inputString.strip()
    if len(newString) == 0:
        return ""
    if newString[len(newString) - 1] == ":":
        newString = newString[0:len(newString) - 1]
        # print("removing :")
    return newString


#Name: readFile
#Role: take a wild guess.
#Input:
#   FN- filename as a string
#Return:
#   readEPs- A big ol' array of all the EPs (populated MAPIs).
#       I don't know what EP means. I forgot shortly after creating the variable and didn't feel like renaming it.
def readFile(FN):
    readEPs = []

    fptr = open(FN, "r")
    currLine = fptr.readline()
    while currLine:
        if re.search("\s+(properties:)", currLine):  # find value of properties
            print(refine(currLine))
            indProperties = getIndent(currLine)
            currLine = fptr.readline()

            while getIndent(currLine) > indProperties:
                boing = MAPI()
                boing.setFN(currLine)
                # print("!"+refine(currLine))
                indMAPI = getIndent(currLine)
                currLine = fptr.readline()

                while getIndent(currLine) > indMAPI:
                    boing.parseData(splitCol(currLine))
                    # print(currLine)
                    currLine = fptr.readline()
                # boing.dispMAPI()
                readEPs.append(boing)
        currLine = fptr.readline()

        # currLine = fptr.readline()

        # Properties has been identified
        # indentValProperties = getIndent(readline)

    print("done reading")
    fptr.close()
    return readEPs

def findTabs(FN):
    fptr = open(FN, "r")
    currLine = fptr.readline()
    lineNo = 0
    while currLine:
        lineNo+=1
        for i in currLine:
            if i == "\t":
                print("tab found on line",lineNo)


        currLine = fptr.readline()


    print("done reading")
    fptr.close()

#Name: getFileName
#Role: ask the user for the file name.
#TODO: make this more intuitive. Maybe just ask for the file via the location... Not too sure.
#TODO: make this work lol
def getFileName():
    return input("What is file name?\n")

#Name: writeEPs
#Role: write EPs to a csv file ordered as they should be
#Inputs:
#   readEPs- all the EPs that have been read and need to be written to the file
#   WFN- the filename to write stuff to
#Return: void
def writeEPs(readEPs, WFN):
    with open(WFN, 'w', newline='') as csvfile:         #THIS LINE CANNOT BE CHANGED. IT IS FORMATTED EXCLUSIVELY TO ADDRESS A BUG WITHIN PYTHON 3
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(readEPs[0].__dict__.keys())
        for EP in readEPs:
            # writing the data rows
            csvwriter.writerow(EP.__dict__.values())

    # print(readEPs[0])
    print("finished writing!")



if __name__ == "__main__":
    # FN = getFileName()
    RFN = "vehicleInspection.raml"
    WFN = "output.csv"
    #readEPs = readFile(RFN)
    #writeEPs(readEPs, WFN)
    findTabs("testfile.raml")

    # getAttributes(readEPs[0])
    # print(readEPs[0].__dict__.keys())
    # print(readEPs[0].__dict__.values())
