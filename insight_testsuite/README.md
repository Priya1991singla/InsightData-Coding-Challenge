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
