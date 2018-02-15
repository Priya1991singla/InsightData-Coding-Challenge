# imported required packages
import pandas as pd
from math import floor
from datetime import datetime
import re
import sys


class PercentileNumericError(Exception):
    """Raised when percentile is not numeric"""
    pass


def data_null_checks(mylist):
    """Checks for null data in input and return the result"""
    if "" in mylist:
        print("Encountered some null data points. Skipping...")
        return(True)
    return(False)


def data_notnull_checks(mylist):
    """Checks for not null value in input list and return the result"""
    if "" not in mylist:
        print("Encountered some unwanted data. Skipping...")
        return(True)
    return(False)


def data_numeric_checks(mylist):
    """Checks if elements in mylist is numeric"""
    for i in mylist:
        if not i.isnumeric():
            print("Encountered some unnumeric data. Skipping...")
            return(True)
    return(False)


def data_alpha_checks(mylist):
    r = re.compile("^[a-zA-Z ,]*$")
    for i in mylist:
        if not r.match(i):
            print("Encountered some non-alphabetic data. Skipping...")
            return(True)
    return(False)


def data_length_checks(mylist, mylengthlist):
    """Checks if the length of element matches with its given list"""
    for i in range(0, len(mylist)):
        if len(mylist[i]) < mylengthlist[i]:
            print("Length of some data points is inappropriate. Skipping...")
            return(True)
    return(False)


def data_convert(mylist, mydatatype):
    """Convert all the data into numeric format"""
    for i in range(0, len(mylist)):
        if mydatatype[i] == datetime:
            mylist[i] = datetime(year=int(mylist[i][-4:]),
                                 month=int(mylist[i][:2]),
                                 day=int(mylist[i][2:4]))
        else:
            mylist[i] = mydatatype[i](mylist[i])
    print("Data conversion is in process...")
    return(mylist)


def data_slice(data, start, end):
    """Convert all the data into required sliced format"""
    data = data[start:end]
    print("Data slicing is in process...")
    return(data)


def check_repeat_donors(unique_donors, zip_code, name):
    """Check if the donor is repeated or not"""
    r = unique_donors.loc[(unique_donors["ZIP_CODE"] == zip_code) &
                          (unique_donors["NAME"] == name)
                          ].index.tolist()
    print("Checking if donor is repeated...")
    return(r)


def write_output_data(file, data):
    """File the output in the required format"""
    print("Formatting output for writing into file.")
    file.write("|".join(data))
    file.write("\n")


def add_unique_donor(unique_list, details):
    """Append the unique donor encountered into the tale"""
    print("Adding unique donor to Dataframe.")
    new_donor = pd.Series(details,
                          ["NAME", "ZIP_CODE", "DATE"])
    return(unique_list.append(new_donor,
                              ignore_index=True))


def check_data_order(new_date, old_date):
    """Check if data is of back-date"""
    if old_date <= new_date:
        return(True)
    print("Back date data found. Skipping...")
    return(False)


def analysis_function():
    """The main function to analyze the input file and write the output file"""
    # reading file names
    print("Reading the file names")
    itcont_filename = sys.argv[1]
    percent_filename = sys.argv[2]
    output_filename = sys.argv[3]

    # catching exceptions in the program
    try:
        # file containing percentile information
        print("Reading percentile")
        f = open(percent_filename, "r")
        percentile = f.read().strip()
        f.close()

        # raise exception if percentile is not numeric
        if not percentile.isnumeric() or percentile == "":
            raise(PercentileNumericError)

        # convert percentile to int
        percentile = data_convert([percentile], [int])[0]

        # create empty dataframe for recording unique donors
        print("Creating table for unique donors registration")
        unique_donors = pd.DataFrame(columns=["NAME", "ZIP_CODE", "DATE"])

        # no. of contributions and list of transaction amt by repeated donors
        count = 0
        amt = []

        # opening output file
        f = open(output_filename, "w")

        # file containing compaign information
        print("Reading all donor details.")
        with open(itcont_filename, "r") as fd:
            for line in fd:

                # split the list on delimiter '|'
                data = line.split("|")

                # defining descriptive variables
                cmte_id = data[0]
                name = data[7]
                zip_code = data[10]
                year = data[13]
                transaction_amt = data[14]
                other_id = data[15]

                # check for null data
                data_check1 = data_null_checks([year, name, cmte_id,
                                                zip_code, transaction_amt])
                if data_check1:
                    continue

                # check for not null data
                data_check2 = data_notnull_checks([other_id])
                if data_check2:
                    continue

                # check for numeric data
                data_check3 = data_numeric_checks([year, zip_code,
                                                   transaction_amt])
                if data_check3:
                    continue

                # check for data lengths
                data_check4 = data_length_checks([zip_code], [5])
                if data_check4:
                    continue

                # check for alphabetical data
                data_check5 = data_alpha_checks([name])
                if data_check5:
                    continue

                # convert data as per needs
                print("Data Conversion Done.")
                year, transaction_amt = data_convert([year, transaction_amt],
                                                     [datetime, float])
                transaction_amt = round(transaction_amt)
                zip_code = data_slice(zip_code, 0, 5)

                # find if repeated donor
                row = check_repeat_donors(unique_donors, zip_code, name)

                # check if repeated donor is found
                if row != []:
                    print("Repeated donor found.")
                    row = row[0]

                    # checking if date is of later date or not
                    date_res = check_data_order(year,
                                                unique_donors.at[row, "DATE"])

                    if date_res:
                        print("Computing for repeated donor...")
                        count += 1

                        # adding new contribution to list
                        amt.append(transaction_amt)

                        # calculating total contribution by repeated donors
                        total = sum(amt)

                        # calculating percentile based on nearest-rank method
                        percent = amt[int(floor(percentile / 100 * count))]

                        # updating unique_donor table with new current date
                        unique_donors.at[row, "DATE"] = year

                        # writing to the output file
                        details = [cmte_id, zip_code, str(year.year),
                                   str(percent), str(total), str(count)]
                        write_output_data(f, details)
                        print("Data written for repeated donor")
                else:
                    # saving data into dataframe to further matching
                    print("Unique donor found.")
                    details = [name, zip_code, year]
                    unique_donors = add_unique_donor(unique_donors, details)

        # closing output file
        f.close()

    # Handling the error related to Input/Output
    except IOError:
        print("Can't file the required files. Verify the path and files")

    # Handling the error related to Percentile
    except PercentileNumericError:
        print("Percentile is not numeric")

if __name__ == "__main__":
    analysis_function()
