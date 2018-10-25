# bme590hrm
####TO RUN:

The main file is hrm_code.py. In order to run a certain file, please go down to
the main() function and change the variable filepath to the appropriate file path. This 
file will import the data and produce two arrays, time and voltage, to perform calculations.
It currently calculates the mean heart rate based on the duration of the entire ECG 
signal; however, a user can input their own duration into the function calc_bpm to change
the duration it uses to calculate bpm. 

####TEST PYTHON SCRIPT:
The test_hrm_code.py is the python file which tests the functions. Currently, coverage is
at 83%. I am still missing a function to test the filter_signal function in hrm_code.py.

####PEAK DETECTION:

My peak detection function works by applying a moving average to the data. This function
is based off of "Analyzing a Discrete Heart Signal Using Python" by Paul van Gent (1).
The user can input an appropriate "window size" at which the function looks at the data.
The function moves across the data, identifying regions where the data is above the moving
average. Once those regions are identified, it looks within those regions to find the
maximum of that region and tags it as a peak.

1. van Gent, P. (2016). Analyzing a Discrete Heart Rate Signal Using Python. A tech blog about fun things with Python and embedded electronics. Retrieved from: http://www.paulvangent.com/2016/03/15/analyzing-a-discrete-heart-rate-signal-using-python-part-1/


####JSON FILES:

.json files can be found in the test_data folder. The code runs for all files, 
except for 28. There are corresponding .json files for all files except for 28, which is 
the cursed file. However, sometimes the moving average does not identify any peaks 
(files 9 and 20) and that definitely is wrong.


####FUTURE (SUNDAY(S)) WORK:

* __Peak Identification:__ The moving average function is not the best way to identify peaks in the signal. I tried
correlation when I was first starting the project; however, I could never compute the correct beat times
even for simple functions so I went with this method. If the data is particularly noisy
or is inverted or negative, the moving average function has issue with it.  

* __Using Classes:__ In order to make my code more efficient, implementing classes would 
be preferable, particularly when testing the function.

* __Complete Test Coverage:__ I still need to test the filter voltage function in order 
to have complete coverage. Also, currently, most of my tests only have one test condition
which is not very thorough.  

* __Exception Handling:__ I throw a couple exceptions in the code. However, I mainly
put warnings in my log instead of dealing with the issue. For example, I alert
the user that the voltage is above normal ECG range, but I do not do anything
to address that warning. This could be improved upon. 