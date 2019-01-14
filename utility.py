# this is the utility file for all the remote management scripts
# this will include functions such as retlist, which doesnt infact return a list

import csv

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
  # This fucntion returns a dictioanry of dictionaries that represent devices
  # elements required include
    # backup
    # managed antivirus
    # patch management
    # type - workstation or server
    # client name
  # dictionary keys will be defined by client, secondary dictionary will be by device name
  dictionary = {}
  with open(filename) as csv_file:
    csv_reader  = csv.reader(csv_file, delimiter=",")
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
        mav = row[39] # 39

        if client in dictionary:
          swaplist = dictionary[client]
          swaplist.append([worksrv, client, site, device, freq, patch, backup, mav])
          dictionary[client] = swaplist
        else:
          dictionary[row[2]] = [[worksrv, client, site, device, freq, patch, backup, mav]]

      line_count += 1
    return dictionary