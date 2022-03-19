# THIS IS THE ONLY SECTION TO BE MODIFIED BY USERS

# change this variable to the location of input data on your device

inputDataLocation = "testInOut/finalInput.js"

# change this variable to the output destination on your device, strongly recommend not to overwrite any existing data

outDestination = "testInOut/testOutput.pde"

# variables------------------------------------------------------------------------------------------------------------

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


# holding string for the output
outputFile = ""

# tracker of position of our trim
mastertrim = -1

dataString = " " + loadFileAsString(inputDataLocation, "r")

# grabbing the length of the string so we can analyze our translation location later
mainStringLength = stringLength(dataString)


# function for finding a keyword and determining our next steps
def findkey(stringWithKey, output):
    # words to search for in the inputfile to begin a translation pattern
    keywords = ["\nvar ", "\nlet ", "\nconst ", " var ", " let ", " const "]

    holdingString = ""
    trimKey = -1
    global mastertrim
    mastertrim = -1

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
            trimKey -= 1
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

# functions----------------------------------------------------------------------------------------------------


# function for finding a keyword and determining our next steps
def findFunctionKey(stringWithKey, output):
    # words to search for in the inputfile to begin a translation pattern
    keywords = ["\nfunction ", " function "]
    holdingString = ""
    trimKey = -1
    global mastertrim
    mastertrim = 0

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

                        # add all non-key characters to the output so we dont lose them
                        for letters in holdingString:
                            if counter < holdingString.find(key) - 1:
                                counter += 1
                                output += letters

                            else:
                                counter += 1

                    # when we find a key that matches what we analyze, determine how to find the name
                    output += trimStringRight(key, 1) + withinParen(stringWithKey, trimKey)
                    trimKey -= 1
                    holdingString = ""

    # restart the process of analysis if we are not at the end of the string
    if trimKey < mainStringLength:
        mastertrim = trimKey
        findFunctionKey(stringWithKey, output)

    output += holdingString

    return output


def withinParen(mainString, trimKey):
    # first, cut this string to the position we left off of
    withParen = trimStringLeft(mainString, trimKey)
    release = ""
    matchingParenCount = 0

    for letter in withParen:
        trimKey += 1
        release += letter

        if letter == "(" or letter == "{":
            matchingParenCount += 1

        if (letter == ")" or letter == "}") and matchingParenCount > 0:
            matchingParenCount -= 1

            if letter == "}" and matchingParenCount == 0:
                global mastertrim
                mastertrim = trimKey
                frontpart = "void "

                if release.find("\nreturn ") > -1 or release.find(" return ") > -1:
                    frontpart = "[DataType] "

                return frontpart + release

# classes----------------------------------------------------------------------------------------------------------


# function for finding a keyword and determining our next steps
def findClass(stringWithKey, output):
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
            key = ""
            if holdingString.find(" class ") > -1:
                key = " class "

            if holdingString.find("\nclass ") > -1:
                key = "\nclass "

            if key != "":
                # focus only on the key to translate
                if holdingString != key:
                    counter = -1

                    # add all non-key characters to the output so we dont lose them
                    for letters in holdingString:

                        if counter < holdingString.find(key) - 1:
                            counter += 1
                            output += letters

                        else:
                            counter += 1

                # when we find a key that matches what we analyze, determine how to find the name
                output += key + findName(stringWithKey, trimKey)

                trimKey -= 1
                holdingString = ""

    # restart the process of analysis if we are not at the end of the string
    if trimKey < mainStringLength:
        mastertrim = trimKey
        findClass(stringWithKey, output)

    return output


# function for grabbing the name of the class
def findName(stringWithName, trimKey):
    className = ""
    stringWithName = trimStringLeft(stringWithName, trimKey)

    # grab the name of the class, end on the first {
    for letter in stringWithName:
        trimKey += 1

        if letter != "{":
            className += letter

        if letter == "{":
            break

    # once we have the name, we can replace "construtor" with it, and determine methods within the brackets
    return className + "{" + translateWithin(stringWithName, trimKey, className)


def translateWithin(stringWithinBrac, trimKey, className):
    # start at one since we're within the first bracket
    matchingParenCount = 1

    # trim the string we seek to analyze
    withinBrac = trimStringLeft(stringWithinBrac, stringLength(className) + 1)

    # temporary string
    holdingString = ""

    # string to return
    output = ""

    # for each letter, see if we find any keys
    for letter in withinBrac:
        holdingString += letter
        trimKey += 1

        # affect the counter
        if letter == "(" or letter == "{":
            matchingParenCount += 1

        if (letter == ")" or letter == "}") and matchingParenCount > 0:
            matchingParenCount -= 1

            if letter == "}":
                output += holdingString
                holdingString = ""

        # we find the constructor, replace with class name
        if holdingString.find("constructor") > -1:
            # add the class name where constructor would be
            output += trimStringRight(holdingString, stringLength(holdingString) - stringLength("constructor"))
            output += className + "("
            holdingString = ""

        # we find "this.", replace with "var" so the variable translator can translate properly
        if holdingString.find("this.") > -1:
            # add " var " in place of " this. "
            output += trimStringRight(holdingString, stringLength(holdingString) - stringLength("this."))
            output += " var "
            holdingString = ""

        # we find "(" while not within another method- beginning of new method
        if letter == "(" and matchingParenCount == 2:
            # create a trim of holdingString that goes up to the next character after the last },
            # then add "void " before the method name
            reverseString = ""
            reverseIndex = stringLength(holdingString) - 1

            # go backwards over holding string until we find the name (whitespace after characters)
            while reverseIndex >= 0:
                charToAnalyse = holdingString[reverseIndex]
                reverseString = charToAnalyse + reverseString

                if charToAnalyse == " " and not reverseString.isspace():
                    calc = stringLength(holdingString) - stringLength(reverseString)
                    methodName = " void" + reverseString
                    output += trimStringRight(holdingString, calc) + methodName
                    break

                reverseIndex -= 1

            holdingString = ""

        # we find "}" while not within another method- end of class
        if letter == "}" and matchingParenCount == 0:
            break

    return output

# trying ---------------------------------------------------------------------------------------------------------------


# run the process
outputString = ""
outputString = trimStringLeft(findClass(dataString, outputString), 1)

# save the outcome to the output file
outFile = open(outDestination, "w")
outFile.write(outputString)
outFile.close()

dataString = " " + loadFileAsString(outDestination, "r")
outputString = ""

outputString = trimStringLeft(findFunctionKey(dataString, outputString), 1)

# save the outcome to the output file
outFile = open(outDestination, "w")
outFile.write(outputString)
outFile.close()

dataString = " " + loadFileAsString(outDestination, "r")
outputString = ""

outputString = trimStringLeft(findkey(dataString, outputString), 1)

# save the outcome to the output file
outFile = open(outDestination, "w")
outFile.write(outputString)
outFile.close()

