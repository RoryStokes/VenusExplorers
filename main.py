from explorer import Explorer
import sys, re, numpy


#defining regular expressions to read in each of the 3 different input line types
gridInitPattern     = re.compile("([0-9]+) ([0-9]+)$")
explorerInitPattern = re.compile("([0-9]+) ([0-9]+) ([NSEW])$")
explorerMovePattern = re.compile("([LRM])*")


######################
#FIRST LINE OF INPUT #
######################

#uses the regular expression to read the first line of input
match = gridInitPattern.match(input())
#if the regex does not match, output an error and quit
if match is None:
	print("Invalid input in line 1. Line should contain: [right coord] [top coord]")
	sys.exit(1)
#extract the grid size from the line. these values are not currently used
right  = int(match.group(1))
top    = int(match.group(2))

#initialise an array of booleans to indicate which grid cells contain explorers
grid   = numpy.full((right,top),False,dtype=bool)



#############################
# SUBSEQUENT LINES OF INPUT #
#############################

#initialise variables
lineNumber = 1
explorers  = []

for line in sys.stdin:

	## LINE 1: INITIALISATION ##

	#Input is converted to upper case to allow for mixed case entry,
	#since behaviour is still well defined
	init = explorerInitPattern.match(line.upper())
	lineNumber += 1

	#if the regex does not match, output an error and quit
	if init is None:
		print("Invalid input in line {}. Line should contain: [x coord] [y coord] [facing direction (N,S,E,W)]".format(lineNumber))
		sys.exit(1)
	#extract the values from the line
	x = int(init.group(1))
	y = int(init.group(2))
	facing = init.group(3)
	#construct the explorer object from the extracted values
	currentExplorer = Explorer(x,y,facing,bounds)
	#store the explorer in a list of explorers
	explorers.append(currentExplorer)


	## LINE 2: MOVEMENT INSTRUCTIONS ##

	#Input is converted to upper case to allow for mixed case entry,
	#since behaviour is still well defined
	line = input().upper()
	lineNumber += 1

	#use regex to confirm that string only contains valid instructions
	move = explorerMovePattern.match(line)
	#if the regex does not match, output an error and quit
	if move is None:
		print("Invalid input in line {}. Line should only contain characters 'L', 'R' and 'M'".format(lineNumber))
		sys.exit(1)

	#iterate through each character and call relevant method on explorer object
	for char in line:
		if char == "L":
			success = currentExplorer.turnLeft()
		elif char == "R":
			success = currentExplorer.turnRight()
		else:
			#Since the line matched the move pattern, the only other option is moving
			success = currentExplorer.move() 
			if currentExplorer.collided():
				print("Warning: Explorer passed through an occupied cell during the instructions in line {}. Possible collision between explorers".format(lineNumber))

		if not success:
			print("Error: Invalid instruction in line {}, terminating".format(lineNumber))
			sys.exit(1)

	#set final grid cell as occupied
	grid[currentExplorer.getX(),currentExplorer.getY()] = True

##########
# OUTPUT #
##########

#defining output format string: two numbers and a single character
outputFormat = "%d %d %s"

#iterate through the explorers in the list
for explorer in explorers:
	#load explorer state
	x = explorer.getX()
	y = explorer.getY()
	facing = explorer.getFacing()

	#confirm getFacing has returned successfully
	if not facing:
		print("Error: Invalid explorer data, terminating".format(lineNumber))
		sys.exit(1)

	#output formatted string
	print(outputFormat % (x, y, facing))