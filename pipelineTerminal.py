"""Data pipeline user terminal"""

'''
This file contains the component for running the user terminal.
The user can navigate through the GUI of the user terminal and conduct various
operations on the imported data. The user terminal include other features such
as exporting the data and saving the data directory and job history record. 
The user terminal also provides an autosave feature that can be enabled.
'''

from pipelineData import Data, DataVisual, Feature_select, save_check
import pipelineUtil as pu
import pipelineGUI as pg
from sysconfig import sys

if __name__ == '__main__':
    print(pg.title)
    # check if users want to enable autosave
    autosave_check = input('Do you wish to enable autosave? Type yes or no ')
    if autosave_check == 'yes':
        _data = Data(auto_save=True)
    else:
        _data = Data()
    _data.import_data() # import data
    mainmenu = False
    
    while True:
        print(pg.function_selection)
        user_input = input('User: ')
        
        if user_input == '1': # enter data cleaning menu
            print(pg.dc)
            _running = True
            while _running is True and mainmenu is False:
                print(pg.data_ops) # display options
                print(pg.option)
                user_input = input('User: ')
                if user_input == '1': # missing data operations
                    while _running:
                        print(pg.missing_data)
                        print(pg.option)
                        user_input = input('User: ')
                        if user_input == '1':
                            _data.check_na() # check nans
                        elif user_input == '2':
                            _data.drop_impute() # drop and impute
                        elif user_input == ';':
                            _data.display_data() # display data
                        elif user_input == '8': # returns to previous menu
                            _running = False
                        # clears data and return to main menu
                        elif user_input == '7': 
                            _data = Data()
                            _data.import_data() # import new data
                            mainmenu = True
                            break
                        elif user_input == '9': # returns to main menu
                            mainmenu = True
                            break
                        elif user_input == '0': # exit application
                            save_check(_data.file_directory, _data.func_order)
                            sys.exit()
                        else:
                            print('Input not recognised, please type again!')
                    _running = True
                elif user_input == '2': # feature operations
                    _data.feature_operation()
                elif user_input == '3': # summary statistics
                    while _running:
                        print(pg.summ_stat_ops) # summary statistics operations
                        print(pg.option)
                        user_input = input('User: ')
                        if user_input == '1':
                            print(_data.summ_stat()) # show summary statistics
                        elif user_input == '2':
                            print(_data.outlier_detect()) # outlier detection
                        elif user_input == ';':
                            _data.display_data()                            
                        elif user_input == '8':
                            _running = False
                        elif user_input == '7':
                            _data = Data()
                            _data.import_data()
                            mainmenu = True
                            break
                        elif user_input == '9':
                            mainmenu = True
                            break
                        elif user_input == '0':
                            # check if user wants to save directory information 
                            # and job history
                            save_check(_data.file_directory, _data.func_order)
                            sys.exit()
                        else:
                            print('Input not recognised, please type again!')
                    _running = True
                elif user_input == ';':
                    _data.display_data()                    
                elif user_input == '8':
                    _running = False
                elif user_input == '7':
                    _data = Data()
                    _data.import_data()
                    mainmenu = True
                elif user_input == '9':
                    mainmenu = True
                    break
                elif user_input == '0':
                    save_check(_data.file_directory, _data.func_order)
                    sys.exit()
                else:
                    print('Input not recognised, please type again!')
            _running = True
            mainmenu = False
            _exit = False
                            
        elif user_input == '2': # enter data visualisation options
            print(pg.dv) 
            _dataviz = DataVisual(_data.df)
            _dataviz.visualise()
        elif user_input == '3': # trigger other functions (feature selection)
            print(pg.fs)
            regressor = input('''Please type in the name of the regressor: ''')
            _feature_select = Feature_select(_data.df, regressor)
            _feature_select.feature_selection()
        elif user_input == '4': # export data
            pu.export_data(_data.df)
        elif user_input == ';': # display data
            _data.display_data()
        elif user_input == '0': # exit application
            save_check(_data.file_directory, _data.func_order)
            sys.exit()
        else:
            print('Input not recognised, please type again!')