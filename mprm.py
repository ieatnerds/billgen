#!/usr/local/bin/python3
# Multi Purpose Remote Management

# Ths will be the main driver for the billgen and diffgen scripts
# utilizing command line arguments in order to be able to use both

#TODO - Add option to give your own ouput file name

import sys, billgen, diffgen

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def help():
  # this funtion will print the help menu for this module
  print("please use -d for diff and -b for billing")
  print("eg:\npython3 mprm.py -d <old.csv> <new.csv>")
  print("python3 mprm.py -b <current.csv>")
  exit()

if len(sys.argv) <= 1:
  help()
else:
  if sys.argv[1] == "-d": # diff
    if len(sys.argv) < 4:
      help()
    else:
      diffgen.main(sys.argv[2], sys.argv[3])
  elif sys.argv[1] == "-b": #billing
    if len(sys.argv) < 3:
      help()
    else:
      billgen.main(sys.argv[2])
  else:
    help()
