# pylint: disable=invalid-name
"""
This module contains the WordCounter class.
This allow to load files and to count how many times word repeat.
"""

import os
import sys
import time

class WordCounter:
    """
    It loads data from a text file and it counts repetance of words.
    It can output the data on a txt or on screen.

    Methods:
        get_data: Returns a list with the original data provided.
        get_errors: Returns a list with the data that were not words.
        count_words: counts how many times word repeats on an array.
        display_count: Displays the word count in console.
        generate_file: Generates a txt file with the word count.
    """
    def __init__(self, file_path):
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
        Validate if the given line from the file is  a word. Return the string or None.
        """
        try:
            return str(line.strip())
        except ValueError:
            return None

    def __load_data(self):
        """
        Loads the data from the provided file, ensuring each line contains a valid string.
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

    def count_words(self, word_list):
        """
        Takes a list and from that list it returns their words and count.
        The words are the keys and the count is how many times they repeat.
        """
        word_count = {}

        for word in word_list:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1

        return word_count

    def __format_conversion_for_display(self):
        """
        Format the conversion for display, returnitng a list of strings.
        Each string represents a row with a the numbers separated by a tab.
        """
        word_count = self.count_words(self.get_data())
        header_file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        formatted_conversion = [f"Row Labels\tCount of {header_file_name}"]

        for key, value in sorted(word_count.items(), key=lambda item: item[1], reverse=True):
            formatted_conversion.append(f"{key}\t{value}")

        formatted_conversion.append(f"Grand Total\t{len(self.get_data())}")

        return formatted_conversion

    def display_conversion(self):
        """
        Display the conversions on terminal.
        """
        formatted_conversions = self.__format_conversion_for_display()
        for line in formatted_conversions:
            print(line)

    def generate_file(self, filename):
        """
        Generate a txt on a tab-separated-value format of the conversions
        """
        formatted_conversions = self.__format_conversion_for_display()

        with open(filename, 'w', encoding='utf-8') as txt_file:
            for line in formatted_conversions:
                txt_file.write(line + '\n')

if __name__ == "__main__":
    print("")
    print("===  Starting analysis === ")
    print("COUNT TABLE:")
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python wordCounter.py fileWithData.txt")
        sys.exit(1)

    FILE_PATH = sys.argv[1]
    word_counter = WordCounter(FILE_PATH)
    word_counter.display_conversion()
    word_counter.generate_file("WordCountResults.txt")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("")
    print(f"Erros found (line, value): {word_counter.get_errors()}")
    print(f"Execution and computation time: {elapsed_time:.4f} seconds")
    print("=== Analysis finished ===")
    print("")
