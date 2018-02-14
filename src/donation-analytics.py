# imported required packages
import pandas as pd
from math import floor
import sys


def data_quality_checks(other_id, year, name,
                        cmte_id, zip_code, transaction_amt):
    """Checks for all the input considerations and return the result"""
    if other_id != "" or year == "" or \
        name == "" or cmte_id == "" or transaction_amt == "" or \
        len(zip_code) < 5 or not zip_code.isnumeric() \
            or not year.isnumeric() or not transaction_amt.isnumeric():
        return(True)
	print("Encountered some corrupt or unwanted data.")
    return(False)


def data_convert(zip_code, year, trans_amt):
    """Convert all the data into required format"""
    zip_code = zip_code[:5]
    year = int(year[4:])
    trans_amt = round(float(trans_amt))
	print("Data conversion is in process...")
    return(zip_code, year, trans_amt)


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
    """Append the unique donor encountered into the DataFrame"""
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
        percentile = int(f.read().strip())
        f.close()

        # create empty dataframe for recording unique donors
		print("Creating dataframe for unique donors registration")
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

                # check for unwanted data
                data_check = data_quality_checks(other_id, year, name,
                                                 cmte_id, zip_code,
                                                 transaction_amt)
                if data_check:
					print("Skipping corrupted data points...")
                    continue

                # convert data as per needs
				print("Data Conversion Done.")
                zip_code, year, transaction_amt = \
                    data_convert(zip_code, year, transaction_amt)

                # find if repeated donor
                row = check_repeat_donors(unique_donors, zip_code, name)

                # check if repeated donor is found
                if row != []:
					print("Repeated donor found.")
                    row = row[0]

                    # checking if date is of later date or not
					date_res = check_data_order(year, int(unique_donors.at[row, "DATE"]))
                    if date_res:
						print("Computing for repeated donor...")
                        count += 1

                        # adding new contribution to list
                        amt.append(transaction_amt)

                        # calculating total contribution by repeated donors
                        total = sum(amt)

                        # calculating percentile based on nearest-rank method
                        percent = amt[int(floor(percentile / 100 * count))]

                        # writing to the output file
                        details = [cmte_id, zip_code, str(year),
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

if __name__ == "__main__":
    analysis_function()
