# 0 CMTE_ID: identifies the flier, which for our purposes is the recipient of this contribution
# 10 ZIP_CODE: zip code of the contributor (we only want the first five digits/characters)
# 13 TRANSACTION_DT: date of the transaction
# 14 TRANSACTION_AMT: amount of the transaction
# 15 OTHER_ID: a field that denotes whether contribution came from a person or an entity

from datetime import datetime
import sys

print str(datetime.now())
print sys.argv

file1 = open (sys.argv[1], "r")
file2 = open (sys.argv[2], "w")
file3 = open (sys.argv[3], "w")

counter = 1
hm_date = {}
hm_zip = {}
for line in file1:
  data = line.split("|")
  data[10] = data[10][:5]
  if len(data[15])<1: #Avoiding lines with Other_ID
  #Calculating per zipcode
    if data[0] in hm_zip:
      count = 0
      if data[10] in hm_zip[data[0]]:
        #Uses Insertion sort to input data
        while count<len(hm_zip[data[0]][data[10]]) and int(data[14])>int(hm_zip[data[0]][data[10]][count]):
          count = count + 1
        hm_zip[data[0]][data[10]].insert(count, int(data[14]))
      else:
        hm_zip[data[0]][data[10]] = []
        hm_zip[data[0]][data[10]].append(int(data[14]))
    else:
      hm_zip[data[0]] = {}
      hm_zip[data[0]][data[10]] = []
      hm_zip[data[0]][data[10]].append(int(data[14]))

    #Calculating median for zipcode   
    l = len(hm_zip[data[0]][data[10]])  
    if l % 2 == 0:
      median = int(round((float(hm_zip[data[0]][data[10]][l/2]) + float(hm_zip[data[0]][data[10]][(l/2) - 1]))/2))
    else:
      median = hm_zip[data[0]][data[10]][l/2]

    file2.write(data[0] + "|" + str(data[10]) + "|" + str(median) + "|" + str(l) + "|" + str(sum(hm_zip[data[0]][data[10]])) + "\n")

    #Calculating per date
    if data[0] in hm_date:
      if data[13] not in hm_date[data[0]]: 
        hm_date[data[0]][data[13]] = []           
    else:
      hm_date[data[0]] = {}
      hm_date[data[0]][data[13]] = []
    hm_date[data[0]][data[13]].append(int(data[14]))
           
    counter = counter + 1
    if counter > 1000000:
      break

sorted_recp = sorted(hm_date.keys()) 
for key in sorted_recp:
  dates = [datetime.strptime(ts, "%m%d%Y") for ts in hm_date[key].keys()]
  dates.sort()
  sorted_dates = [datetime.strftime(ts, "%m%d%Y") for ts in dates] 
  for date in sorted_dates:
    sorted_list = sorted(hm_date[key][date])
    l = len(sorted_list)
    if l % 2 == 0:
      median = int(round((float(sorted_list[l/2]) + float(sorted_list[(l/2) - 1]))/2))
    else:
      median = sorted_list[l/2]      
    file3.write(key + "|" + str(date) + "|" + str(median) + "|" + str(len(sorted_list)) + "|" + str(sum(sorted_list)) + "\n")
print str(datetime.now())
file1.close()
file2.close()
file3.close()
