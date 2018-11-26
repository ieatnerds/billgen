# This python script will read through a remote management inventory report
# and be able to generate customer billing.

# it will also be able to diff between an old report and a new report
# in order to find machines that have fallen off of remote management

import csv, os, subprocess, sys
from utility import *

def clientmach(listof):
  # enumerate the clients and return how many machines they have
    # worksrv = 0
    # client = 1
    # site = 2
    # device = 3
    # freq = 4
    # patch = 5
    # backup = 6
    # MAV = 7
  newdict = {}
  for key in listof:
    total_wk = 0
    workstations = 0 # with rm
    servers = 0 # with rm
    sbackups = 0 # servers
    wbackups = 0 # workstations
    mav = 0 # total MAV
    # machs is list of devices
    machs = listof[key]
    for item in machs:
      # item is list of elements for that device
      
      if item[0] == "workstation":
        total_wk += 1
        if not ((item[7] == "Not Installed") or (item[7] == "Not Compatible")): # mav
          mav += 1
        if not ((item[6] == "Not Installed") or (item[6] == "Not Compatible")): # backup
          wbackups += 1
        if not (item[5] == "Not Installed"): # rm
          workstations += 1
        
      else: # servers
        if item[7] != "Not Installed": # mav
          mav += 1
        if item[6] != "Not Installed": # backups
          sbackups += 1 
        if not (item[5] == "Not Installed"): # rm
          servers += 1
    
    print(bcolors.HEADER, key, ": ", bcolors.ENDC)
    
    print(bcolors.OKBLUE, "     ","Total Workstations:  ", total_wk, "  WRKSTN: ", workstations, "  SRVR: ", servers, " MAV: ", mav, "  WBCKP: ", wbackups, " SBCKP: ", sbackups, bcolors.ENDC)
   
    newdict[key] = [total_wk, workstations, servers, mav, wbackups, sbackups]
  return newdict
  

def writecsv(dictionary, outputname):
  # this function will export our dictionary dictionary list into a csv file for andrew
  try:
    open(outputname, 'w').close()
  except:
    print("Epic fail!")
    #exit()

  with open(outputname, "a") as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow(["client", "Total Workstations", "RM Workstations", "RM Servers", "Managed AV", "Workstation Backup", "Server Backups"])
    for key in dictionary:
      truelist = [key] + dictionary[key]
      wr.writerow(truelist)


def main(filename, outputname="billing.csv"):
  dictionary = retlist(filename)
  csvdict = clientmach(dictionary)
  writecsv(csvdict, outputname)
  if sys.platform.startswith('darwin'):
    subprocess.call(('open', outputname))
  elif os.name == 'nt': # For Windows
    os.startfile(outputname)
  elif os.name == 'posix': # For Linux, Mac, etc.
    subprocess.call(('xdg-open', outputname))

#main(outputname = "notbilling.csv")
