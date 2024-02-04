#!/usr/bin/env python3
# pylint: disable=invalid-name
"""
This module contains the NumberConverter class.
This allows to convert numbers to binary and hexadecimal base. 
"""

import os
import sys
import time

class NumberConverter:
    """
    It loads data from a text file and converts numbers
    to binary and hex. It can output the data on a txt or on screen.

    Methods:
        get_data: Returns a list with the original data provided.
        get_errors: Returns a list with the data that was not numeric
        convert_to_hex: transforms one number to binary
        convert_to_binary: transforms one number to hexadecimal
        transform_data: Uses the hex and binary methos to transform the whole dataset
        display_conversion: Displays the conversion in console.
        generate_file: Generates a txt file with the conversions.
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
            return int(line.strip())
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

    def convert_to_binary(self, number, bits=10):
        """
        Converts a number to its binary representation.
        For negative numbers, computes the Two's Complement manually.
        """
        if number == 0:
            return '0'

        binary_digits = []
        n = abs(number)

        while n > 0:
            binary_digits.append(str(n % 2))
            n = n // 2

        # Reverse the list and join to form the binary string

        if number < 0:
            # Compute Two's Complement for negative numbers
            binary = ''.join(binary_digits[::-1]).zfill(bits)
            return self.__twos_complement(binary, bits)

        binary = ''.join(binary_digits[::-1])
        return binary

    def __twos_complement(self, binary, bits):
        """
        Computes the Two's Complement of a binary string. 
        Inverts the digits and adds one to the result.
        """
        # Invert the digits
        inverted = ''.join('1' if b == '0' else '0' for b in binary)

        # Add one to the inverted binary string
        inverted_plus_one = self.__binary_add_one(inverted)

        # Ensure the result is of the desired length
        return inverted_plus_one.zfill(bits)

    def __binary_add_one(self, binary):
        """
        Adds one to a binary string.
        """
        binary_list = list(binary)
        length = len(binary_list)
        carry = 1

        for i in range(length - 1, -1, -1):
            if binary_list[i] == '1' and carry == 1:
                binary_list[i] = '0'
                carry = 1
            elif carry == 1:
                binary_list[i] = '1'
                carry = 0
                break

        if carry == 1:
            binary_list.insert(0, '1')

        return ''.join(binary_list)[-length:]

    def convert_to_hex(self, number):
        """
        Converts a number directly to its hexadecimal representation, 
        padding with 'F's for negative to extend to proposed method in test-cases.
        """
        # Handling zero as a special case
        if number == 0:
            return '0'

        hex_digits = '0123456789ABCDEF'
        hex_string = ''
        n = abs(number)

        # Direct conversion to hexadecimal for positive numbers
        while n > 0:
            hex_string = hex_digits[n % 16] + hex_string
            n = n // 16

        # Extend the hexadecimal to 10 hex characters for negatives
        if number < 0:
            hex_string = hex_string.rjust(10, '0')
            inverted_hex = ''.join(hex_digits[15 - hex_digits.index(digit)] for digit in hex_string)
            hex_string = self.__add_one_to_hex(inverted_hex).rjust(10, 'F')

        return hex_string

    def __add_one_to_hex(self, hex_string):
        """
        Adds one to a hexadecimal string.
        """
        hex_digits = '0123456789ABCDEF'
        result = ''
        carry = 1

        for digit in reversed(hex_string):
            if carry == 0:
                result = digit + result
                continue

            index = hex_digits.index(digit) + carry
            if index >= 16:
                result = '0' + result
                carry = 1
            else:
                result = hex_digits[index] + result
                carry = 0

        return result

    def transform_data(self):
        """
        Iterates over all the data and transform it.
        """
        transformed_data = [(data,
                  self.convert_to_binary(data),
                  self.convert_to_hex(data)
                  ) for data in self.data
            ]
        return transformed_data

    def __format_conversion_for_display(self):
        """
        Format the conversion for display, returnitng a list of strings.
        Each string represents a row with a the numbers separated by a tab.
        """
        conversions = self.transform_data()
        header_file_name = os.path.splitext(os.path.basename(self.file_path))[0]
        formatted_conversion = [f"NUMBER\t{header_file_name}\tBIN\tHEX"]

        for i, value in enumerate(conversions):
            formatted_conversion.append(f"{i + 1}\t{value[0]}\t{int(value[1])}\t{value[2]}")\

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
    print("CONVERTION TABLE:")
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        sys.exit(1)

    FILE_PATH = sys.argv[1]
    converter = NumberConverter(FILE_PATH)
    converter.display_conversion()
    converter.generate_file("ConvertionResults.txt")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("")
    print(f"Erros found (line, value): {converter.get_errors()}")
    print(f"Execution and computation time: {elapsed_time:.4f} seconds")
    print("=== Analysis finished ===")
    print("")
