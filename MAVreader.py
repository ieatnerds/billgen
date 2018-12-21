import utility
import csv


def createmess(filename):
  dictlist = utility.retlist(filename)
  dictlist2 = {}
  #client2 = []
  for key in dictlist:
    client = dictlist[key]
    for comp in client:
      if comp[7] != "Active":
        comp2 = comp
        # Get rid of unneeded information in list
        del comp2[0] 
        del comp2[3] # remove 4 - 1
        del comp2[3] # Remove 5 - 2
        del comp2[3] # remove 6 - 3
        if key in dictlist2:
          holder = dictlist2[key]
          holder.append(comp2)
          dictlist2[key] = holder

        else:
          dictlist2[key] = [comp2]
      
  return dictlist2


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
        truelist = second_key
        wr.writerow(truelist)


def main(filename):
  mess = createmess(filename)
  writecsv(mess, "mavissues.csv")


main()