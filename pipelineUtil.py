'''Data pipeline utility functions'''

'''
This file contains all the utiliy functions that support the data operations
and the user terminal. It includes class wrappers and functions that store the 
information of the functions/methods called. It also includes functions for
exporting and autosaving the data.
'''

from copy import deepcopy
from collections import defaultdict
import dill

# a logging class that stores a class method object when the method is called
class log:
    
    def __init__(self, func):
        self.func = func
        
    def __call__(self, *args):
        self.func(*args)

# same class but stores the class method arguments in a dictionary        
class log_col:
    
    def __init__(self, func):
        self.func = func
        self.ops = {}
        
    def __call__(self, *args):
        self.func(*args)
        arg_list = []
        for arg in args:
            arg_list.append(arg) # append all arguments to a list
        arg_list.pop(0) # remove the first element which is the self idiom
        for i in arg_list:
            self.ops[self.func] = i # add the second argument to the dictionary

# stored the class method arguments in a defaultdict            
class log_args:
    
    def __init__(self, func):
        self.func = func
        self.ops = defaultdict(list)
        
    def __call__(self, *args):
        self.func(*args)
        arg_list = []
        for arg in args:
            arg_list.append(arg)
        arg_list.pop(0)
        for i in arg_list:
            # add all the arguments to the defaultdict
            self.ops[self.func].append(i) 

# function storage with no arguments
def func_store(log_func, func_order):
    # makes a deepcopy of the method object from the logging class 
    # original logging object can now be manipulated
    copy_log_func = deepcopy(log_func.func)
    # append the method to the function call order list
    func_order.append(copy_log_func) 

# function storage with one argument
def func_store_col(log_func, func_order):
    copy_log_func_ops = deepcopy(log_func.ops)
    func_order.append(copy_log_func_ops)

# function storage for multiple arguments
def func_store_range(log_func, func_order, num_args):
    copy_log_func_ops = deepcopy(log_func.ops)
    func_order.append(copy_log_func_ops)
    # remove the arguments in the dictonary in the logging class
    # dictionary becomes empty and ready for the next method call
    for i in range(num_args):
        log_func.ops[log_func.func].pop()

    # export function
def export_data(df):
    # lets the user choose the file type, directory and file name
    # currently only supports csv and xlsx files
    file_type = input('Please select your export format: 1. CSV 2. XLSX')
    directory = input('Please type in the directory you wish to export to: ')
    file_name = input('Please type in the filename: ')
    if file_type == '1':
        combine = (directory, '/', file_name, '.csv')
        destination = ''.join(combine)
        df.to_csv(destination)
        print('Data exported!')
    elif file_type == '2':
        # lets the user choose the sheet name for a xlsx file
        sheet = input('Please type in the name of the sheet: ')
        combine = (directory, '/', file_name, '.xlsx')
        destination = ''.join(combine)
        df.to_excel(destination, sheet_name=sheet)
        print('Data exported!')
    else:
        raise TypeError('Type not specified/included')

# autosave function   
def autosave(df, directory, sheet, func_order, enabled=False):
    # overrides data provided in the initial file destination
    if enabled is True:
        if '.csv' in directory: # check the file type
            df.to_csv(directory)
        else:
            df.to_excel(directory, sheet_name=sheet)
        with open('autosave_job.pkl', 'wb') as f:
            dill.dump(func_order, f)
        print('Autosaved!')