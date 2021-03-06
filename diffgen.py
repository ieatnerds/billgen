# this module will be able to produce a diff csv containing all the machines that used to be on 
# remote management dashboard. 

# to test I used two inventory reports to find which devices were on the older report, but not upon the 
# newer report. I removed several devices manually to make sure there were machines to find.

# Theres also the possibilty of finding the new machines that were found.

import csv, os, subprocess, sys
from utility import retlist


def writecsv(dictionary, outputname):
  # this function will export our dictionary dictionary list into a csv file for andrew
  try:
    open(outputname, 'w').close()
  except:
    print("Epic fail!")
  with open(outputname, "a") as f:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    #wr.writerow(["client", "Total Workstations", "RM Workstations", "RM Servers", "Managed AV", "Workstation Backup", "Server Backups"])
    for key in dictionary:
      for second_key in dictionary[key]:
        truelist = dictionary[key][second_key]
        wr.writerow(truelist)

def compdiff(olderdict, newerdict):
  # this function will take the two dictionaries and spit out 
  # a new single dictionary of the all the machines that are only in the old 
  # dictionary
  diffdict = {}
  for company_key in olderdict.keys():
    #print(company_key)
    
    if company_key not in newerdict:
      diffdict[company_key] = {}
      holder = olderdict[company_key]

      for device_key in holder:
        #print("DEVICE_KEY: ", device_key)
        #print(type(holder))
        diffdict[company_key][device_key] = holder[device_key]
    else:
      diffdict[company_key] = {}
      holder = olderdict[company_key]
      holder2 = newerdict[company_key]
      for device_key in holder:
        #print(device_key)
        if device_key not in holder2:
          subdict = diffdict[company_key]
          subdict[device_key] = holder[device_key]
          
  return diffdict


def main(oldfile, newfile, outputname="diffout.csv"):
  olddict = retlist(oldfile)
  newdict = retlist(newfile)
  #csvdict = clientmach(dictionary)
  #print(type(olddict))
  #print(newdict)
  diffdict = compdiff(olddict,newdict)
  #print(diffdict)
  writecsv(diffdict, outputname)
  if sys.platform.startswith('darwin'):
    subprocess.call(('open', outputname))
  if os.name == 'nt': # For Windows
    os.startfile(outputname)
  elif os.name == 'posix': # For Linux, Mac, etc.
    subprocess.call(('xdg-open', outputname))


#main()
