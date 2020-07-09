'''Data pipeline automation'''

'''
This file contains the automation component of the pipeline.
The data directory and job history (function calls) records are imported to
automatically prepare and save the data under the actions recorded in the
user terminal.
This file should be executed separately with the user terminal. Its sole
purpose is to automate the entire data preparation process conducted through
the user terminal so that the user does not need to use the user terminal
again for the same operations. 
'''

from pipelineData import Data
from pipelineGUI import data_direc_import, job_hist_import, data_loc
import collections
import dill    

if __name__ == '__main__':
    
    # Prompts the user to type in the directories of the data directory file
    # and job history
    directory_input = input(data_direc_import)
    job_history_input = input(job_hist_import)
    
    # check the file type
    if '.pkl' not in job_history_input:
        raise OSError("[Errno 9] Bad file number")
    else:
        # assign variables to the data directory and job history lists
        with open(directory_input) as d:
            directory_file = [line.rstrip() for line in d]
        with open(job_history_input, 'rb') as l:
            job_history_file = dill.load(l)
            
        # check for the length of the data directory list
        # for csv files, there will only be one element in the list 
        # which is the directory name
        if len(directory_file) < 2: 
            _data = Data(directory=directory_file[0])
        else:
            # for xlsx files, there will be more than one element in the list
            # first element is the directory name, second is the sheet name
            _data = Data(directory=directory_file[0], sheet=directory_file[1])

        _data.direct_import() # import the data directly
        
        # iterate over the job history list
        for func in job_history_file:
            if callable(func) is True: 
                func(_data) # call the function directly if it is callable
            elif type(func) is dict:
                # assign a list that contains the key (function)
                key_list = list(func) 
                # assign a variable that contains the function in the list
                f = key_list[0] 
                params = func[f] # assign a variable that contains the argument
                f(_data, params) # call the function with its argument
            elif type(func) is collections.defaultdict:
                key_list = list(func)
                f = key_list[0]
                params = func[f]
                if len(params) == 2:
                    # set two variables to represent the two arguments
                    x = params[0]
                    y = params[1]
                    f(_data, x, y)
                elif len(params) == 3:
                    # set three variables to represent the three arguments
                    x = params[0]
                    y = params[1]
                    z = params[2]
                    f(_data, x, y, z)
            
        df = _data.df # assign the prepared the dataframe to a variable
        print('Data prepared! \n')
        
        # prompts the user where to save the prepared data
        save_data = input(data_loc)
        # check for csv or xlsx file format
        if '.csv' in save_data: 
            df.to_csv(save_data)
            print('Data saved!')
        elif '.xlsx' in save_data:
            sheet = input('Please type in the sheet name: ')
            df.to_excel(save_data, sheet_name=sheet)
            print('Data saved!')
        else:
            raise NameError('Incorrect file format')