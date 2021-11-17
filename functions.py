from variables import trimStringLeft, trimStringRight, stringLength, loadFileAsString

# words to search for in the inputfile to begin a translation pattern
keywords = ["\nfunction ", " function "]

# holding string for the output
outputFile = ""

# tracker of position of our trim
mastertrim = 0

# load the file that needs to be translated
dataString = " " + loadFileAsString("testInOut/variableInput.js", "r")

# grabbing the length of the string so we can analyze our translation location later
mainStringLength = stringLength(dataString)


# function for finding a keyword and determining our next steps
def findFunctionKey(stringWithKey, output):
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


# run the process
outputFile = trimStringLeft(findFunctionKey(dataString, outputFile), 1)

# save the outcome to the output file
outFile = open("testInOut/testOutput.pde", "w")
outFile.write(outputFile)
outFile.close()