#
# first part of the translator, used to translate variable declarations
#

# function to trim strings from the left given an index
def trimstring(toTrim, trimIndex):
    currentIndex = -1
    cutString = ""
    for letter in toTrim:
        currentIndex += 1
        if currentIndex >= trimIndex:
            cutString += letter
    return cutString


# words to search for in the inputfile to begin a translation pattern
keywords = ["var ", " var ", " var "]

# holding string for the output
outputFile = ""

# variable to hold the length of the input
mainStringLength = 0

# tracker of position of our trim
mastertrim = -1

# load the file that needs to be translated
inputFile = open("testInOut/testInput.js", "r")
data = ""
with inputFile as myInput:
    data = myInput.readlines()
print(data)
inputFile.close()

# turn the loaded data into one string
dataString = ""
for section in data:
    dataString += section
print(dataString)

for letters in dataString:
    mainStringLength += 1


def findkey(stringWithKey, output):
    holdingString = ""
    trimKey = -1
    global mastertrim
    for letter in stringWithKey:
        print("trimkey insude = " + str(trimKey))
        if trimKey < mastertrim:
            trimKey += 1

        if trimKey >= mastertrim:
            holdingString += letter
            trimKey += 1
            # check what we have against all possible keys
            print("current view: " + holdingString)
            for key in keywords:
                if holdingString == key:
                    if key == "var " or key == "/n var":
                        nameStop = "="
                        output += findname(stringWithKey, trimKey, nameStop) + "\n"
                        trimKey -= 1
                        holdingString = ""

    if trimKey < mainStringLength:
        print("Trimkey: " + str(trimKey))
        mastertrim = trimKey
        findkey(stringWithKey, output)

    return output



def findname(stringWithName, trimKey, namestop):
    withname = trimstring(stringWithName, trimKey)
    holdingstring = ""
    global mastertrim
    for letter in withname:
        if letter != namestop:
            holdingstring += letter
            trimKey += 1
        if letter == namestop:
            trimKey += 1
            holdingstring += letter
            break
    mastertrim = trimKey
    return findtype(stringWithName, trimKey, ";", holdingstring)


def findtype(stringWithType, trimkey, typestop, prevname):
    withtype = trimstring(stringWithType, trimkey)
    holdingstring = ""

    # collect the type text
    for letter in withtype:
        if letter != typestop:
            holdingstring += letter
            trimkey += 1
        if letter == typestop:
            trimkey += 1
            break

    # determine the type of the text
    typetype = ""
    # all numbers means int
    stripstring = holdingstring.strip()
    print("stripped = " + stripstring)
    if stripstring.isdigit():
        typetype = "int"
    # if " is found, its a string
    if stripstring.find('"') > -1:
        typetype = "String"
    # if true or false is found
    if stripstring.find("true") > -1 or stripstring.find("false") > -1:
        typetype = "boolean"
    # if . is found but no ", float
    if stripstring.find('"') == -1 < stripstring.find("."):
        typetype = "float"
    # otherwise, just keep the same?
    if typetype == "":
        typetype = "var"

    # put the strings together
    returnstring = typetype + prevname + holdingstring + typestop
    global mastertrim
    mastertrim = trimkey
    return returnstring


outputFile = findkey(dataString, outputFile)

print("outputfile: " + "-" + outputFile + "-")

outFile = open("testInOut/testOutput.pde", "w")
outFile.write(outputFile)
outFile.close()