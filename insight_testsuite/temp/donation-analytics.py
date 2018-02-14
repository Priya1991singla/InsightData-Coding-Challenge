# imported required packages
import pandas as pd
from math import floor
import sys

# reading file names
itcont_filename = sys.argv[1]
percent_filename = sys.argv[2]
output_filename = sys.argv[3]

# file containing percentile information
f =  open(percent_filename,"r")
percentile = int(f.read().strip())
f.close()

# create empty dataframe
mydata = pd.DataFrame(columns = ["NAME","ZIP_CODE","DATE"])

# no. of contributions and list of transaction amt by repeated donors
count = 0 
amt = []

# opening output file
f = open(output_filename,"w") 

# file containing compaign information
with open(itcont_filename,"r") as fd:
    for line in fd:
        
        # split the list on delimiter '|'
        data = line.split("|")
        
        # check for unwanted data
        if data[15] != "" or data[13] == "" or data[7] == "" or data[13] == "" or data[0] == "" or data[14] == "" or len(data[10]) < 5:
            continue
        
        # convert data as per needs
        data[10] = data[10][:5]
        data[13] = int(data[13][4:])
        data[14] = int(data[14])
        
        # find if repeated donor
        row = mydata.loc[(mydata["ZIP_CODE"] == data[10]) & (mydata["NAME"] == data[7])].index.tolist()
        
        # check if repeated donor is found
        if row != []:
            row = row[0]
            
            # checking if date is of later date or not
            if int(mydata.at[row,"DATE"]) <= data[13]:
                count += 1
                
                # adding new contribution to list
                amt.append(data[14])
                
                # calculating total contribution by repeated donors
                total = sum(amt)
                
                # calculating percentile based on nearest-rank method
                percent = amt[int(floor(percentile / 100 * count))]
                
                # writing to the output file
                f.write("|".join([data[0],data[10],str(data[13]),str(percent),str(total),str(count)]))
                f.write("\n")
        else:
            # temporarily saving data into dataframe to further matching
            new_series = pd.Series([data[7],data[10],data[13]],["NAME","ZIP_CODE","DATE"])
            mydata = mydata.append(new_series,ignore_index=True)

# closing output file
f.close()
