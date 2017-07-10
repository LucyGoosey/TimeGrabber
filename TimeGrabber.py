# ######################################################################### #
#                                                                           #
#    This program is free software: you can redistribute it and/or modify   #
#    it under the terms of the GNU General Public License as published by   #
#    the Free Software Foundation, either version 3 of the License, or      #
#    (at your option) any later version.                                    #
#                                                                           #
#    This program is distributed in the hope that it will be useful,        #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#    GNU General Public License for more details.                           #
#                                                                           #
#    You should have received a copy of the GNU General Public License      #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                           #
# ######################################################################### #

import os
import sys
import pyperclip
from datetime import timedelta

# import solution
# return solution.solve(problem)
# Why isn't this working?!
# Fuck sake, let's do it the hard way...

# ############################################# #
#                 Time Functions                #
# ############################################# #

# Grabs the lines from the clipboard, input file or asks the user for a file to parse
def GetLines():
    global FILEPATH
    
    # If we have a command line argument, assume it is the filepath
    if len(sys.argv) == ONE + ONE:  # Best line is best line.
        FILEPATH = sys.argv[ONE]
            
    # If we don't have a command line argument, or if it isn't a file, check the clipboard...
    if not os.path.isfile(FILEPATH) or os.path.isdir(FILEPATH):
        cb = pyperclip.paste()
        if not cb is None:          # If the clipboard has text in it...
            return cb.split("\n")  #   ...split it at the newline and send it back!

    # If the clipboard didn't contain text, and the input file isn't valid...
    while not os.path.isfile(FILEPATH) or os.path.isdir(FILEPATH):
        print("That isn't a file!")
        # ...ask the user for a file!
        FILEPATH = input("Please type a (relative) path to the file containing the times: ")
            
    # Stupid Michealsoft Binbows
    FILEPATH.replace("\\", "/")
            
    # If we're reading from a file, we should output to a file too (for consistency)
    global OUTPUT_TO_FILE
    OUTPUT_TO_FILE = True
        
    # Open our file and grab all the lines
    f = open(FILEPATH, 'r')
    lines = f.readlines()
    f.close()
    
    return lines
    
# Gets the difference in time between the obtained times
def GetTimeDiffs(lines):
    out = []
    
    for l in lines:
        times = GetTimesFromLine(l)
        if times != None and len(times) == ONE + ONE:
            out.append(GetDifferenceInTime(times[ZERO], times[ONE]))
        
    return out
    
# Attempts to parse a line and retrieve the times as strings
def GetTimesFromLine(l):
    # Split the line using our time separator
    out = l.split(START_END_SEPARATOR)
        
    # If we aren't left with just two values...
    if len(out) != ONE + ONE:
        print("Improperly formatted line: " + l)
        return None
    
    # Clean off any whitespace surrounding the time
    for t in out:
        t = t.strip()
        
    return out

# Parses two times represented as strings and returns the difference in time between them
def GetDifferenceInTime(t1, t2):
    # Split the time using the separator, and convert the strings into a timedelta object
    splTime = t1.split(TIME_SEPARATOR)
    t1 = timedelta(hours = int(splTime[ZERO]), minutes = int(splTime[ONE]))
    
    splTime = t2.split(TIME_SEPARATOR)
    t2 = timedelta(hours = int(splTime[ZERO]), minutes = int(splTime[ONE]))
    
    # Let timedelta do all the heavy lifting
    d = t2 - t1
    
    if d.days < 0:
        d += timedelta(days = -d.days)
        
    return d
    
# Takes a list of timedeltas and returns the accumulated total time
def GetTotalTime(tDiff):
    out = timedelta()
    
    for td in tDiff:
        out += td
    
    return out
    
# ############################################# #
#               Output Functions                #
# ############################################# #
    
# Takes a timedelta and returns a nicely formatted string
def FormatTime(t):
    hours, r = divmod(t.seconds, SECS_IN_HOUR)
    minutes, seconds = divmod(r, SECS_IN_MINUTE)
    
    hours += t.days * 24
    
    out = ""
    
    if hours != ZERO:
        out = "{0} hours and ".format(str(hours))
    
    out += "{0} minutes".format(str(minutes))
    
    return out
    
# Takes the original line and the index of a difference in time and returns them in a nicely formatted string
def FormatLine(l, i):
    l = l.lstrip().rstrip()
    return "{0} \t// {1}\n".format(l, FormatTime(timeDiff[i]))
    
# Outputs the obtained data to the clipboard
def GetOutput(totalTime):
    out = ""
    
    # Add the original lines along with the difference in times
    i = ZERO
    for l in lines:
        if START_END_SEPARATOR in l and TIME_SEPARATOR in l:
            out += FormatLine(l, i)
            i += ONE
        else:
            out += l
        
    # Add the total time
    out += "\nTotal time: " + FormatTime(totalTime)
    return out
    
# ############################################# #
#                  Main Script                  #
# ############################################# #

# Constants
START_END_SEPARATOR = "-"
TIME_SEPARATOR      = ":"
SECS_IN_HOUR        = 3600
SECS_IN_MINUTE      = 60
HOURS_IN_DAY        = 24
ZERO                = 0    # Hehe, no magic numbers here!
ONE                 = 1

# File related variables
FILEPATH            = ""
OUTPUT_TO_FILE      = False

# Grab the individual lines from the clipboard or the file we are loading
lines = GetLines()
# If we have no lines, we have nothing to process!
if len(lines) == ZERO:
    print("ERROR: No lines found!")
    sys.exit()

# Parses the lines and gets any time differences it can extract
timeDiff = GetTimeDiffs(lines)
# If we haven't found any time differences, there's nothing we can do!
if len(timeDiff) == ZERO:
    print("\nERROR: No times found in provided lines!")
    sys.exit()
    
totalTime = GetTotalTime(timeDiff)
    
out = GetOutput(totalTime)
# Formats the obtained information, and sends it to wherever it needs to go!
if OUTPUT_TO_FILE:
    # We output to a file named FILEPATH_.ext (where ext is the file's original extension)
    outFilepath = FILEPATH[:FILEPATH.rfind(".")] + "_" + FILEPATH[FILEPATH.rfind("."):]
    
    with open(outFilepath, 'w') as outFile:
        outFile.writelines(out)
else:
    pyperclip.copy(out)