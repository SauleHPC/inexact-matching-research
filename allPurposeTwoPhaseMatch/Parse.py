import gzip
import xml.etree.ElementTree as ET
from Callback import Callback
import sys
import os
import json
import csv
from Kmer import mer_builder


class MyObject:
    def __init__(self, **kwargs):
        self.id = 0
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __repr__(self):
        return str(self.__dict__)


'''
@brief: Used to parse through CSV file.

@author: Davis Spradling
'''

'''
Used to parse through files.

@param: file_name - File that is being parsed.

@param: callback - Methods you want to be executed every time a paper is parsed.

@param: callback - Maximum number of lines that will be parsed.

@param: file_associated_attributes - Attributes that will be associated at the end of output when done for file being parsed.

'''

def parse_file(file_name, file_key, callback, max_lines, file_associated_attributes=None):
    if file_associated_attributes is None:
        file_associated_attributes = []
        
    file_associated_attributes.append(file_key)
    i = 0

    with open(file_name, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            obj_data = {attr: row[attr] for attr in file_associated_attributes if attr in row}
            obj = MyObject(**obj_data)
            i += 1
            obj.id = i 
            for function in callback:
                function(obj)

            # Check if the line count exceeds max_lines
            if max_lines is not None and i >= max_lines:
                break



