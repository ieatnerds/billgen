# This python script will read through a remote management inventory report
# and be able to generate customer billing.

# it will also be able to diff between an old report and a new report
# in order to find machines that have fallen off of remote management

import csv, time, datetime, os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def retlist(filename):
  #This fucntion returns a dictioanry of dictionaries that represent devices
  # elements required include
    # backup
    # managed antivirus
    # patch management
    # type - workstation or server
    # client name
  # dictionary keys will be defined by client, secondary dictionary will be by device name
  dictionary = {}
  with open(filename) as csv_file:
    csv_reader= csv.reader(csv_file, delimiter=",")
    line_count = 0
    dictionary = {}
    for row in csv_reader:
      if line_count == 0:
        pass # skip header
      else:
        # there are 44 fields included in the inventory report
        worksrv = row[1] # 1
        client = row[2] # 2
        site = row[3] # 3
        device = row[4] # 4
        freq = row[9] # 9
        patch = row[33] # 33
        backup = row[38] # 38
        mav = row[40] # 39

        if client in dictionary:
          swaplist = dictionary[client]
          swaplist.append([worksrv, client, site, device, freq, patch, backup, mav])
          dictionary[client] = swaplist
        else:
          dictionary[row[2]] = [[worksrv, client, site, device, freq, patch, backup, mav]]

      line_count += 1
    return dictionary


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
    
    #print(bcolors.HEADER, key, ": ", bcolors.ENDC)
    
    #print(bcolors.OKBLUE, "     ","Total Workstations:  ", total_wk, "  WRKSTN: ", workstations, "  SRVR: ", servers, " MAV: ", mav, "  WBCKP: ", wbackups, " SBCKP: ", sbackups, bcolors.ENDC)
   
    newdict[key] = [total_wk, workstations, servers, mav, wbackups, sbackups]
  return newdict
  

def writecsv(dictionary, outputname):
  # this function will export our dictionary dictionary list into a csv file for andrew
  try:
    open(outputname, 'w').close()
  except:
    print("Epic fail!")

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


#main()
