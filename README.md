# js-pde-translator

The completed translator is now complied into "allTogether.py", utilizing the 3 translation parts mentioned below. Now begins my testing with more data!

#

Parts of a simple translator to turn JavaScript files into Processing files. Given some structural similarities between the languages and my previous use of both for similar projects, I wanted to experiment with a translation algotrithm. 

Part 1 is a basic translator for variable declarations, where I attempt to find a variable's declaration and determine what data type the variable is.

Part 2 is a translator for function declarations, where I attempt to determine if a function returns a value. If so, the prefix [DataType] is added to indicate the need for specification. Otherwise, add "void".

Part 3 is a translator for Classes, where I attempt to change the terms "constructor" to the class name, "this." to "var " to be see by the Variable Translator, and add a "void " prefix to methods. 
