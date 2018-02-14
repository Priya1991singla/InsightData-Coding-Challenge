# InsightData-Coding-Challenge
Contains solution files for coding challenge given by InsightData

# Table of Contents
1. [Overview](README.md#overview)
2. [Problem Statement](README.md#problem-statement)
3. [Methodology] (README.md#methodology)
3. [Testing](README.md#testing)


# Overview

This repository is made for the purpose of presenting participation in coding challenege by InsightData (Data Engineering).
The analysis code is written in Python which use the package `pandas` and `math`.

# Problem Statement

For this challenge, we're asked to take a file listing individual campaign contributions for multiple years, determine which ones came from repeat donors, calculate a few values and distill the results into a single output file, `repeat_donors.txt`.

For each recipient, zip code and calendar year, we calculated these three values for contributions coming from repeat donors:

* total dollars received
* total number of contributions received 
* donation amount in a given percentile

The political consultants, who are primarily interested in donors who have contributed in multiple years, are concerned about possible outliers in the data. So they have asked that the program allow for a variable percentile. That way the program could calculate the median (or the 50th percentile) in one run and the 99th percentile in another.

All other details of the challenge and files used in it can be found at https://github.com/InsightDataScience/donation-analytics

# Methodology

To solve this challenge, we follow the concept of modularity. We created methods for each and every thing so that the program can be scaled at any point in future.
The following steps are followed to solve the challenge:

* Create an empty table for keeping record of unique donors
* Create following variables:
	* `count`: Initialize with 0. Keeps count of repeated donors
	* `amt`: Empty List to record transaction amount of repeated donors
* Read the input files i.e. percentile.txt and itcont.txt
* While reading every line from the itcont file, do the following:
	* Split the line on `|`
	* Define every needed element as descriptive variable
	* Perform checks for unwanted and corrupt data
	* If unwanted data is found then skip and read next line
	* Convert the data into desirable data types
	* Check if the name and zip code of the new encountered donor matches with any donor registered in `unique_donor` table
	* If no match is found then add the new donor details to `unique_donor` table and read the next line from file
	* If match is found then check if the data is using back date from registered date or not
	* If data is from back date then skip and read next line from file
	* If data is not from back date then increment the `count` variable by 1, add the transaction amount to `amt` variable and calculate the percentile for so far encountered repeated donors using nearest-rank method
	* Write all the needed details of the so far encountered repeated donors in the needed format to the output file i.e. repeat_donors.txt
* Close all the opened files

The methods created are as follows:

* data_quality-checks(): This function takes the data to be checked according to the input considerations given and return whether or not the data is acceptable for further computation
* data_convert(): This function takes zip code, year and transaction amount and convert it into desired data type
* check_repeat_donors(): This function checks the donor details in `unique_donor` table to find repeated donors 
* add_unique_donor(): This function add the unique donor details in the `unique_donor` table
* check_data_order(): This function helps in mapping out of order data. If some donor details are from back date then they are skipped in order to maintain the current computation
* write_output_data(): This function format the repeated donor details in order to write in the output file
* analysis_function(): This function use the all above functions to read the input, calculate all the needed measures and write them to the output file.

# Testing

### Pre-requisite:

Make sure you have the following installed before testing:

* Python
* Pandas (Python package)
* Math (Python package)

Create a new folder `test_n` in `insight_testsuite\tests` folder. Create two more folders as `input` and `output` in the folder `test_n`. Put your version of both the input files (`percentile.txt` and `itcont.txt`) and output file (`repeat_donors.txt`) in these folder.

### On Linux:

To test on Linux,

Open the shell and traverse to the path of `insight_testsuite` folder and run the following statement:

	insight_testsuite~$ ./run_tests.sh

On a failed test, the output of `run_tests.sh` should look like:

    [FAIL]: test_n
    [Sat Feb 3 16:28:01 PDT 2018] 0 of 1 tests passed

On success:

    [PASS]: test_n
    [Sat Feb 3 16:25:57 PDT 2018] 1 of 1 tests passed
	
### On Windows:

To test the program on Windows,

Open the command prompt and traverse to the path of `insight_testsuite\tests\test_n` and run the following statement:

	insight_testsuite\tests\test_n> python ../../../src/donation-analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt

The output file `repeat_donors.txt` can be checked in output folder.
