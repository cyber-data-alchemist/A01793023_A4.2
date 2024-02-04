# A4.2 - Programming Exercise 1

## Overview

**TC470.10**

**A01793023 - Jorge Luis Arroyo Chavelas**

Here is the code to run 3 programas, one for generating basic stats, one for transform decimal numbers to binary and to hex and one to count repeated words. All of these files are based on reading a file and they were created to pass PEP8 and requirements tests.

## Usage

Each program is designed to be invoked from the command line with a single file as an input parameter. The general invocation format is as follows:
 
``` bash
python <program_name>.py <input_file>
```

Where <program_name> is one of computeStatistics, convertNumbers, or wordCount, and <input_file> is the path to the file containing the data to be analyzed.

**computeStatistics.py**
Computes and prints descriptive statistics (mean, median, mode, standard deviation, variance) for a list of numbers provided in a file.

**convertNumbers.py**
Converts numbers from a file to their binary and hexadecimal representations, printing the results to the console and saving them to a file.

**wordCount.py**
Counts the frequency of each distinct word in a provided text file, displaying the counts on the console and saving them to a file.

## Test Cases

Each program comes with a set of test cases to validate its functionality:

P1: Test cases for computeStatistics.py, focusing on its ability to accurately compute statistical measures.
P2: Test cases for convertNumbers.py, ensuring accurate conversion of numbers to binary and hexadecimal formats.
P3: Test cases for wordCount.py, designed to verify the correct counting of word frequencies in various text file scenarios.

## PEP8 Considerations
The code within these files aims to comply with PEP8 standards wherever possible, with exceptions made primarily for file naming and certain variable names to align with specific task requirements. To ensure code quality and readability, pylint is used with certain checks disabled (e.g., invalid-name) to accommodate these exceptions without compromising the overall adherence to Python's style guide.