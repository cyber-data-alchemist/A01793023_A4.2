#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
This module contains the ComputeStatistics class.
This allow to load files and to show statistics of a provided file.
"""

import os
import sys
import time

class ComputeStatistics:
    """
    It loads data from a text file and generate statistics.
    The file should contain a number per line and be utf-8 encoded.

    Methods:
        get_data: Returns the validated numerical data as a list.
        get_errors: Returns a list of lines that could not be converted to valid numerical data.
        compute_count: Returns the count of valid numerical data points.
        compute_mean: Calculates and returns the mean of the data.
        compute_median: Calculates and returns the median of the data.
        compute_mode: Identifies and returns the mode(s) of the data.
        compute_variance: Calculates and returns the variance of the data.
        compute_stddev: Calculates and returns the standard deviation of the data.
        get_stats: Aggregates and returns all computed statistics as a dictionary.
        display_stats: Prints the computed statistics to the console in a human-readable format.
        generate_file: Generates a txt file with the computed statistics at the specified filename.
    """

    def __init__(self, file_path):
        """
        Initiates the class with a file path and it stores the data and the line errors.
        """
        self.file_path = file_path
        self.data = []
        self.line_errors = []
        self.__load_data()

    def __validate_file_exists(self):
        """
        Check if the file exists. If not, raise an error.
        """
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")

    def __validate_input(self, line):
        """
        Validate if the given line from the file is a number. Return the number or None.
        """
        try:
            return float(line.strip())
        except ValueError:
            return None

    def __load_data(self):
        """
        Loads the data from the provided file, ensuring each line contains a valid number.
        Invalid lines are ignored on data and stored in line_errors.
        """
        self.__validate_file_exists()

        with open(self.file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                number = self.__validate_input(line)
                if number is not None:
                    self.data.append(number)
                else:
                    self.line_errors.append((i, line))

    def get_data(self):
        """
        Returns the loaded data.
        """
        return self.data

    def get_errors(self):
        """
        Returns the errors in the loading process.
        """
        return self.line_errors

    def compute_count(self):
        """
        Calculate the length of data.
        """
        return len(self.data)

    def compute_mean(self):
        """
        Calculate the mean of data.
        """
        n = self.compute_count()
        if n == 0:
            return 0
        return sum(self.data) / n

    def compute_median(self):
        """
        Calculate the median of data.
        """
        sorted_data = sorted(self.data)
        n = self.compute_count()
        mid = n // 2

        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        return sorted_data[mid]

    def compute_mode(self):
        """
        Determine the mode of data.
        """
        return max(set(self.data), key=self.data.count)

    def compute_variance(self):
        """
        Calculate the variance of data.
        """
        mean = self.compute_mean()
        if len(self.data) == 0 or len(self.data) - 1 == 0:
            return 0
        return sum((x - mean) ** 2 for x in self.data) / ( len(self.data) - 1 )

    def compute_stddev(self):
        """
        Calculate the standard deviation of data.
        """
        variance = self.compute_variance()
        return variance ** 0.5


    def get_stats(self):
        """
        Returns the stats of data.
        """
        COUNT = self.compute_count()
        MEAN = self.compute_mean()
        MEDIAN = self.compute_median()
        MODE = self.compute_mode()
        SD = self.compute_stddev()
        VARIANCE = self.compute_variance()
        return {
            "COUNT": COUNT,
            "MEAN": MEAN,
            "MEDIAN": MEDIAN,
            "MODE": MODE,
            "SD": SD,
            "VARIANCE": VARIANCE 
        }

    def __format_stats_for_display(self):
        """
        Format the computed statistics for display, returning a list of strings.
        Each string represents a row with a statistic name and its value, separated by a tab.
        """
        stats = self.get_stats()
        header_file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        formatted_stats = [f"TC\t{header_file_name}"]

        for stat, value in stats.items():
            formatted_stats.append(f"{stat}\t{value}")

        return formatted_stats

    def generate_file(self, filename):
        """
        Generate a txt on a tab-separated-value format of the stats
        """
        formatted_stats = self.__format_stats_for_display()

        with open(filename, 'w', encoding='utf-8') as txt_file:
            for line in formatted_stats:
                txt_file.write(line + '\n')

    def display_stats(self):
        """
        Display the computed statistics.
        """
        formatted_stats = self.__format_stats_for_display()

        for line in formatted_stats:
            print(line)

if __name__ == "__main__":
    print("")
    print("===  Starting analysis === ")
    print("STATS:")
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        sys.exit(1)

    FILE_PATH = sys.argv[1]
    file_stats = ComputeStatistics(FILE_PATH)
    file_stats.display_stats()
    file_stats.generate_file("StatisticsResults.txt")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("")
    print(f"Erros found (line, value): {file_stats.get_errors()}")
    print(f"Execution and computation time: {elapsed_time:.4f} seconds")
    print("=== Analysis finished ===")
    print("")
