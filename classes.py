from variables import trimStringLeft, trimStringRight, stringLength, loadFileAsString

# tracker of position of our trim
mastertrim = -1

# load data
dataString = " " + loadFileAsString("testInOut/classInput.js", "r")

# grabbing the length of the string so we can analyze our translation location later
mainStringLength = stringLength(dataString)

# final string
outputString = ""


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
    stringWithName = trimStringLeft(stringWithName, trimKey+1)

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


# run the process
outputString = trimStringLeft(findClass(dataString, outputString), 1)

# save the outcome to the output file
outFile = open("testInOut/testOutput.pde", "w")
outFile.write(outputString)
outFile.close()


