# javascript_meets_python

This is an interpreter of a mixup language between python and javascript. It has the syntax of javascript and functions of python.
I wrote this because I was searching for a sandboxed python or a secure way to run python with restrictions. It seems like python wasn't created with sandboxing in mind. So, I wrote this in the goal of securing python functions and writing an interpreter. "Free two birds with one key" ;)

# TODO:

#### add methods to calls. example: requests.get("something") --> requests.get("something").text ...
#### replace calls with their return values. example: print(add(1,2)) --> print(3) --> 3
#### look for blocks inside blocks
#### eval blocks

# Currently:

#### every new call/variable... must be in a new line
#### you can't use double quotes inside a double quote string, same thing as single quotes. (can be fixed with a better regex)
#### you need to use double quotes inside a dictionary just like json.
