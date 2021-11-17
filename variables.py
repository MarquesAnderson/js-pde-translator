#
# first part of the translator, used to translate variable declarations
#

# function to trim strings from the left given an index
def trimStringLeft(toTrim, trimIndex):
    currentIndex = -1
    cutString = ""

    for letter in toTrim:
        currentIndex += 1
        if currentIndex >= trimIndex:
            cutString += letter

    return cutString


def trimStringRight(toTrim, trimLength):
    output = ""

    for letter in toTrim:
        if stringLength(output) < trimLength:
            output += letter

    return output


def stringLength(toMeasure):
    lengthS = 0

    for letters in toMeasure:
        lengthS += 1

    return lengthS


def loadFileAsString(fileName, howToRead):
    inputLoad = open(fileName, howToRead)

    with inputLoad as myInput:
        data = myInput.readlines()

    inputLoad.close()
    dataStr = ""

    for section in data:
        dataStr += section

    return dataStr


# words to search for in the inputfile to begin a translation pattern
keywords = ["\nvar ", "\nlet ", "\nconst ", " var ", " let ", " const "]

# holding string for the output
outputFile = ""

# variable to hold the length of the input
mainStringLength = 0

# tracker of position of our trim
mastertrim = -1

dataString = " " + loadFileAsString("testInOut/variableInput.js", "r")

# grabbing the length of the string so we can analyze our translation location later
mainStringLength = stringLength(dataString)


# function for finding a keyword and determining our next steps
def findkey(stringWithKey, output):
    holdingString = ""
    trimKey = -1
    global mastertrim

    # loop over each character in the string
    for letter in stringWithKey:

        if trimKey < mastertrim:
            trimKey += 1

        # if our position in the string is after parts we've already translated,
        # add to our analysis string
        if trimKey >= mastertrim:
            holdingString += letter
            trimKey += 1

            # check what we have against all possible keys
            for key in keywords:

                if holdingString.find(key) > -1:

                    # focus only on the key to translate
                    if holdingString != key:
                        counter = -1

                        for letters in holdingString:

                            if counter < holdingString.find(key) - 1:
                                counter += 1
                                output += letters

                            else:
                                counter += 1

                    # when we find a key that matches what we analyze, determine how to find the name
                    nameStop = "="
                    output += trimStringRight(key, 1) + findname(stringWithKey, trimKey, nameStop)
                    trimKey -= 1
                    holdingString = ""

    # restart the process of analysis if we are not at the end of the string
    if trimKey < mainStringLength:
        mastertrim = trimKey
        findkey(stringWithKey, output)

    output += holdingString

    return output


# gather the name of the variable
def findname(stringWithName, trimKey, namestop):

    withname = trimStringLeft(stringWithName, trimKey)
    holdingstring = ""
    global mastertrim

    # add letters to the name until we find the char that tells us to stop
    for letter in withname:

        if letter != namestop:
            holdingstring += letter
            trimKey += 1

        if letter == namestop:
            trimKey += 1
            holdingstring += letter
            break

        if letter == ";":
            trimKey += 1
            mastertrim = trimKey
            return "var" + holdingstring

    mastertrim = trimKey
    return findtype(stringWithName, trimKey, ";", holdingstring)


# determine the type of the variable based on the data
def findtype(stringWithType, trimkey, typestop, prevname):
    withtype = trimStringLeft(stringWithType, trimkey)
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
    stripstring = holdingstring.strip().strip(")").strip("(")
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

    # if "new" is found, then its an object, so copy object name as data type
    if stripstring.find("new") > -1:
        tempcut = ""

        for letter in stripstring:
            if tempcut.find("new ") == -1:
                tempcut += letter

            elif letter != "(":
                typetype += letter

            elif letter == "(":
                break

    # otherwise, just keep the same?
    if typetype == "":
        typetype = "var"

    # put the strings together
    returnstring = typetype + prevname + holdingstring + typestop
    global mastertrim
    trimkey -= 1
    mastertrim = trimkey
    return returnstring


# run the process
outputFile = trimStringLeft(findkey(dataString, outputFile), 1)

# save the outcome to the output file
outFile = open("testInOut/testOutput.pde", "w")
outFile.write(outputFile)
outFile.close()
