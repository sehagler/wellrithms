This project consists of 3 Python scripts - main.py, image_processor.py, and text_processor.py.  The code is executed by invoking main.py.  Note that the two tasks are activated or deactivated by setting them to True or False.  text_processor.py and image_processor.py specify the objects for carrying out tasks 1 and 2 respectively.  The objects are created in main.py and the sequence the methods are called are given in main.py.  The code assumes the scripts are all in the same directory and that directory contains a folder /data which contains the relevant data to be used and to which output data are written.

Task 1

The code reads the data from the relevant xlsx file.  

The code then proceeds to perform a series of string manipulations and string comparisons to identify a set of likely groups.  This process assumes that most strings tend to go from more general to more specific information and that we are trying to isolate the most general identifying information in the set of strings.  The algorithm performs the following steps.  First, it trims the tail of each item.  This means that it identifies alphanumeric strings at the end of the string that look like specific information like measured sizes or serial numbers or the like and removes them.  Second, it takes the strings and replaces them with the shortest name matches.  That is it takes each string and searches the list of strings and finds the shortest string that matches the initial or final part of the string and replaces the string with this.  Third, it takes the string and replaces them with single name matches.  That is it takes each string and search the list of string to see if there is a single word element in that list which matches any word in the string and replaces the string with this.  Fourth, it takes each string consisting of more than one word and replaces with any common initial component.  Essentially this takes the string and looks at the intersection of the initial portion with initial portions of other strings in the list and replaces the string with the longest intersection.  Finally it performs the second and third steps again.  At the end of this process we have a set of candidate groups to place the strings in.

The code then takes the set of trimmed strings (i.e. the resulting strings after applying step 1 of the procedure in the preceding paragraph) and assigns them to one of the groups extracted in the procedure given in the preceding paragraph.  It does this using a fuzzy string matching algorithm.  The matching is done using Python's FuzzyWuzzy package.  The resulting match is scored from 0 to 100.

The results are output in data/output.xlsx.  There are 8752 strings assigned to 228 groups.  The file contains two sheets with the indicated columns:

	group_assignments

		raw_text - the text given in the original data file
		trimmed_text - the text given after trimming more specific information from the end of the string.
		extracted_group - the group extracted from this string by the group extraction algorithm.
		assigned_group - the group the string is assigned to by the fuzzy matching algorithm.
		assignment_score - the score given the assignment (0-100)
	
	groups

		extracted_groups - the groups extracted by the group extraction algorithm
		num_assigned - the number of string assigned to the given group

Task 2

The code reads the 3 images from the relevant pdf file.	

The code reads the 3 images into a dictionary of numpy arrays.  It then cleans up the images using Python's OpenCV package.  First, it maps each image into black-and-white binary images (i.e. just black or white and no greys).  Second, it removes vertical lines from each image.  Third, it removes horizontal lines from each image.  This ideally will leave a clean text for OCR.  The code goes ahead and OCRs the images using Python's DocTR package.

There is a function to return the cleaned up images as Pandas data frames if needed.

The 3 cleaned up images are output as data/image_0.png, data/image_1.png, and data/image_2.png.
