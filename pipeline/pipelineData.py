"""Data pipeline data classes"""

'''
This file contains all the functionalities for data storage, cleaning, 
engineering, visualisation and other operations. It also include a save 
function for saving the data directory and job history records.
'''

import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection  import train_test_split
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV
from sklearn.feature_selection import RFE
import matplotlib.pyplot as plt
import seaborn as sns 
from sysconfig import sys
import dill
import pipelineUtil as pu
import pipelineGUI as pg

# Data class which contains the data and supports various operations
class Data:
    
    def __init__(self, df=None, directory=None, sheet=None, auto_save=False,
                 func_order=None, file_directory=None):
        if df is None:
            df = pd.DataFrame()
        self.df = df # contains the data frame object
        self.running = True
        self.summ = defaultdict(dict) # a dictionary for storing outliers
        # contains the directory where the data is located
        self.directory = directory 
        self.sheet = sheet # contains the sheet name
        self.auto_save = auto_save
        # a list to store the function call order (job history)
        if func_order is None:
            func_order = []
        self.func_order = func_order
        # a list to store the directory information of the data
        if file_directory is None:
            file_directory = []
        self.file_directory = file_directory
    
    # import data
    def import_data(self):
        print('Import data: ')
        file_type = input('Please indicate the type of file: 1. CSV 2. XLSX ')
        # choice of choosing between csv or excel file type
        if file_type == '1':
            self.directory = input(pg.data_directory)
            self.df = pd.read_csv(self.directory)
            self.file_directory.append(self.directory)
        elif file_type == '2':
            self.directory = input(pg.data_directory)
            self.sheet = input(pg.data_sheet)
            self.df = pd.read_excel(self.directory, sheet_name = self.sheet)
            self.file_directory.append(self.directory)
            self.file_directory.append(self.sheet)
    
    # import dataset directly        
    def direct_import(self):
        if self.sheet is None:
            self.df = pd.read_csv(self.directory)
        else:
            self.df = pd.read_excel(self.directory, sheet_name = self.sheet)
    
    # display the data on screen        
    def display_data(self):
        print(self.df)
    
    # remove features by individual columns
    @pu.log_col
    def remove_col(self, feature_list):
        for col in feature_list:
            try:
                del self.df[col]
            except:
                raise KeyError('cannot find feature')
        return self.df
    
    # remove feature by range
    @pu.log_args            
    def remove_range(self, start_col, end_col):
        try:
            self.df = self.df.drop(self.df.loc[:, start_col: end_col].columns,
                                   axis=1)
            return self.df
        except:
            raise KeyError('cannot find feature')
    
    # standardisation by individual columns
    @pu.log_col
    def mean_norm_col(self, feature_list):
        for col in feature_list:
            try:
                self.df[col] = ((self.df[col]-self.df[col].mean())
                                /self.df[col].std())
            except:
                raise KeyError('cannot find feature')
        return self.df
    
    # standardisation by range
    @pu.log_args
    def mean_norm_range(self, start_col, end_col):
        # obtain the index location of the start and end columns
        start_idx = self.df.columns.get_loc(start_col)
        end_idx = self.df.columns.get_loc(end_col)
        
        for i in range(start_idx, end_idx + 1): # loop by index range
            try:
                self.df.iloc[:, i] = ((self.df.iloc[:, i]
                -self.df.iloc[:, i].mean())/self.df.iloc[:, i].std())
            except:
                raise KeyError('cannot find feature')
        return self.df
    
    # min-max normalisation by individual columns
    @pu.log_col
    def minmax_norm_col(self, feature_list):
        for col in feature_list:
            try:
                self.df[col]=((self.df[col]-self.df[col].min())
                              /(self.df[col].max()-self.df[col].min()))
            except:
                raise KeyError('cannot find feature')
        return self.df
    
    # min-max normalisation by range
    @pu.log_args
    def minmax_norm_range(self, start_col, end_col):
        start_idx = self.df.columns.get_loc(start_col)
        end_idx = self.df.columns.get_loc(end_col)
        
        for i in range(start_idx, end_idx + 1):
            try:
                self.df.iloc[:, i]=((self.df.iloc[:, i]
                -self.df.iloc[:, i].min())
                /(self.df.iloc[:, i].max()-self.df.iloc[:, i].min()))
            except:
                raise KeyError('cannot find feature')
        return self.df
    
    # normalisation choice method        
    def normalise(self, feature_list, start_col, end_col, _range=False):
        # _range determines whether normalisation is by individual column/range
        while True:
            print(pg.feature_norm)
            print(pg.back_exit)
            options = input('User: ')
            if options == '1' and _range == False:
                self.mean_norm_col(self, feature_list)
                pu.func_store_col(self.mean_norm_col, self.func_order)
                break
            elif options == '2' and _range == False:
                self.minmax_norm_col(self, feature_list)
                pu.func_store_col(self.minmax_norm_col, self.func_order)
                break
            elif options == '1' and _range == True:
                self.mean_norm_range(self, start_col, end_col)
                pu.func_store_range(self.mean_norm_range, self.func_order, 2)
                break
            elif options == '2' and _range == True:
                self.minmax_norm_range(self, start_col, end_col)
                pu.func_store_range(self.minmax_norm_range, self.func_order, 2)
                break
            elif options == ';':
                self.display_data()
            elif options == '9': 
                break # returns to the previous menu
            elif options == '0':
                # saving directory 
                # and function calls (job history) to log files
                save_check(self.file_directory, self.func_order)
                sys.exit() # exit the application
            else:
                print('Input not recognised, please type again!')
    
    # mean transformation by individual columns 
    # (taking the mean of different columns) 
    @pu.log_args
    def mean_trans_col(self, feature_list, new_col):
        try:
            self.df[new_col] = self.df[feature_list].mean(axis=1)
        except:
            raise KeyError('cannot find feature')
        return self.df
                
    # mean transformation by range
    @pu.log_args
    def mean_trans_range(self, start_col, end_col, new_col):
        start_idx = self.df.columns.get_loc(start_col)
        end_idx = self.df.columns.get_loc(end_col)
        try:
            self.df[new_col]=self.df.iloc[:, start_idx:end_idx + 1].mean(axis=1)
            return self.df
        except:
            raise KeyError('cannot find feature')
            
    # interquartile range transformation
    @pu.log_args
    def iqr_trans_col(self, feature_list, new_col):
        # if entry is larger than 2, cannot calculate IQR
        if len(feature_list) > 2: 
            raise ValueError('list length is too large')
        else:
            try:
                self.df[new_col] = np.abs(self.df[feature_list[1]]
                                            -self.df[feature_list[0]])
            except:
                raise KeyError('cannot find feature')
        return self.df
    
    # transforming percentages to whole numbers by individual columns
    @pu.log_args
    def percent2whole_col(self, feature_list, new_col):
        for col in feature_list:
            try:
                self.df[col] = (self.df[col]/100)*self.df[new_col]
            except:
                raise KeyError('cannot find feature')
        return self.df
                
    # transforming percentages to whole numbers by range
    @pu.log_args
    def percent2whole_range(self, start_col, end_col, new_col):
        start_idx = self.df.columns.get_loc(start_col)
        end_idx = self.df.columns.get_loc(end_col)
        
        for i in range(start_idx, end_idx + 1):
            try:
                self.df.iloc[:, i] = (self.df.iloc[:, i]/100)*self.df[new_col]
            except:
                raise KeyError('cannot find feature')
        return self.df        
    
    # transformation choice method           
    def multi_transform(self, feature_list, start_col, end_col, _range=False):
        while True:
            print(pg.feature_trans)
            print(pg.back_exit)
            options = input('User: ')
            col_name = input('Please type in the new/base column name: ')
            if options == '1' and _range == False:
                self.mean_trans_col(self, feature_list, col_name)
                pu.func_store_range(self.mean_trans_col, self.func_order, 2)
                break
            elif options == '2' and _range == False:
                self.iqr_trans_col(self, feature_list, col_name)
                pu.func_store_range(self.iqr_trans_col, self.func_order, 2)
                break
            elif options == '3' and _range == False:
                self.percent2whole_col(self, feature_list, col_name)
                pu.func_store_range(self.percent2whole_col, self.func_order, 2)
                break
            elif options == '1' and _range == True:
                self.mean_trans_range(self, start_col, end_col, col_name)
                pu.func_store_range(self.mean_trans_range, self.func_order, 3)
                break
            elif options == '3' and _range == True:
                self.percent2whole_range(self, start_col, end_col, col_name)
                pu.func_store_range(self.percent2whole_range, self.func_order, 3)
                break
            elif options == ';':
                self.display_data()
            elif options == '9':
                break
            elif options == '0':
                save_check(self.file_directory, self.func_order)
                sys.exit()
            else:
                print('Input not recognised, please type again!')
    
    # rename a feature
    @pu.log_args            
    def col_rename(self, feature, feature_new):
        try:
            self.df.rename({feature: feature_new}, axis=1, inplace=True)
        except:
            raise KeyError('cannot find feature')
        return self.df

    # rename by list
    @pu.log_col
    def data_rename(self, feature_list):
        i = 0
        for col in feature_list:
            self.df.rename({self.df.columns.values[i]: col}, axis=1, inplace=True)
            i += 1
        return self.df
    
    # label encoding by individual columns
    @pu.log_col
    def label_class_col(self, feature_list):
        le = LabelEncoder()
        for col in feature_list:
            try:
                self.df[col] = le.fit_transform(self.df[col])
            except:
                raise KeyError('cannot find feature')
        return self.df
    
    # label encoding by range
    @pu.log_args            
    def label_class_range(self, start_col, end_col):
        le = LabelEncoder()
        start_idx = self.df.columns.get_loc(start_col)
        end_idx = self.df.columns.get_loc(end_col)
        
        for i in range(start_idx, end_idx + 1):
            try:
                self.df.iloc[:, i] = le.fit_transform(self.df.iloc[:, i])
            except:
                raise KeyError('cannot find feature')
        return self.df
    
    # menu for choosing the type of feature operations    
    def feature_operation(self):
        
        while self.running:
            print(pg.feature_ops)
            print(pg.back_exit)
            operations = input('User: ')
            if operations == ';':
                self.display_data()
                break
            elif operations == '9':
                break
            elif operations == '0':
                save_check(self.file_directory, self.func_order)
                sys.exit()
            elif operations == '4': # trigger rename method
                print(pg.rename_type)
                print(pg.back_exit)
                user_input = input('User: ')
                if user_input == '1':
                    feature_old = input(pg.feature_rename)
                    feature_new = input('Please type in the new feature name: ')
                    self.col_rename(self, feature_old, feature_new)
                    pu.func_store_range(self.col_rename, self.func_order, 2)
                    # autosaves the data after the operation executes if enabled
                    pu.autosave(self.df, self.directory, self.sheet,
                                self.func_order, enabled=self.auto_save)
                    print('Feature renamed!')
                elif user_input == '2':
                    list_file = input(pg.list_d)
                    # input the list into the file
                    with open(list_file) as f:
                        feature_names = [line.rstrip() for line in f]
                    self.data_rename(self, feature_names)
                    pu.func_store_col(self.data_rename, self.func_order)
                    pu.autosave(self.df, self.directory, self.sheet,
                                self.func_order, enabled=self.auto_save)
                    print('Feature(s) renamed!')
                    break
            elif operations == '1' or '2' or '3' or '5':
                feature_list = []
                feature = str()
                range_select = str()
                # asks the user how do they want to select their features
                range_select = input(pg.range_option)

                if range_select == '1':
                    print(pg.select_fin)
                    while feature != '*': # ends selection when user type '*'
                        feature = input(pg.select_fea)
                        if feature == '*':
                            break
                        else:
                            # append user input to a list
                            feature_list.append(feature) 
                    print('Feature(s) selected: ')
                    print(feature_list) # shows the selection
                    # trigger different feature operations based on user choice
                    if operations == '1':
                        self.remove_col(self, feature_list)
                        pu.func_store_col(self.remove_col, self.func_order)
                        print('Feature(s) deleted!')
                    elif operations == '2':
                        self.normalise(feature_list, None, None)
                        print('Feature(s) normalised!')
                    elif operations == '3':
                        self.multi_transform(feature_list, None, None)
                        print('Feature(s) transformed!')
                    elif operations == '5':
                        self.label_class_col(self, feature_list)
                        pu.func_store_col(self.label_class_col, self.func_order)
                        print('Feature(s) encoded!')
                    else:
                        print('Input not recognised, please type again!')
                
                elif range_select == '2':
                    # asks the user the range of columns they wish to select
                    start_col = input('Please type in the starting feature: ')
                    end_col = input('Please type in the ending feature: ')
                    print('Feature range: ')
                    print(start_col, end_col)
                    if operations == '1':
                        self.remove_range(self, start_col, end_col)
                        pu.func_store_range(self.remove_range, self.func_order, 2)
                        print('Feature(s) deleted!')
                    elif operations == '2':
                        self.normalise(None, start_col, end_col, 
                                       _range=True)
                        print('Feature(s) normalised!')
                    elif operations == '3':
                        self.multi_transform(None, start_col, end_col,
                                             _range=True)
                        print('Feature(s) transformed!')
                    elif operations == '5':
                        self.label_class_range(self, start_col, end_col)
                        pu.func_store_range(self.label_class_range, self.func_order, 2)
                        print('Feature(s) encoded!')                    
                    else:
                        print('Input not recognised, please type again!')
                # autosaves data if enabled
                pu.autosave(self.df, self.directory, self.sheet, 
                            self.func_order, enabled=self.auto_save)
                
            else:
                print('Input not recognised, please type again!')
            
            print('\n')
            print(self.df) # show data
            # set running to True for the running of other operations
        self.running = True 
    
    # drop all nans
    @pu.log
    def drop_all(self):
        self.df = self.df.dropna()
        return self.df
    
    # drop by subset feature
    @pu.log_col    
    def drop_subset(self, col):
        try:
            self.df = self.df.dropna(subset=[col])
        except:
            raise KeyError('cannot find feature')
        return self.df
    
    # impute by column means
    @pu.log    
    def impute_col(self):
        self.df = self.df.fillna(self.mean())
        return self.df
    
    # impute by row means
    @pu.log    
    def impute_row(self):
        self.df = self.df.apply(lambda row: row.fillna(row.mean()), axis=1)
        return self.df
    
    # impute by user defined value on a feature
    @pu.log_args
    def impute_num(self, num, col):
        try:
            self.df[col] = self.df[col].fillna(num)
        except:
            raise KeyError('cannot find feature')
        return self.df

    @pu.log_args
    def impute_zero(self, start_col, end_col):
        start_idx = self.df.columns.get_loc(start_col)
        end_idx = self.df.columns.get_loc(end_col)

        for i in range(start_idx, end_idx + 1):
            try:
                self.df.iloc[:, i] = self.df.iloc[:, i].fillna(0)
            except:
                raise KeyError('cannot find feature')
        return self.df

    # drop or impute data
    def drop_impute(self):
        while self.running:
            print(pg.drop_imp)
            print(pg.back_exit)
            option = input('User: ')
            # lets user choose between dropping nans or impute
            
            if option == '1':
                print(pg.all_subset)
                print(pg.back_exit)
                drop_type = input('User: ')
                # lets user choose to drop all or by subsets
                if drop_type == '1':
                    self.drop_all(self)
                    pu.func_store(self.drop_all, self.func_order)
                    pu.autosave(self.df, self.directory, self.sheet, 
                                self.func_order, enabled=self.auto_save)
                    break
                elif drop_type == '2':
                    # lets user choose which subset to drop
                    col = input('Please type in the subset you wish to drop: ')
                    self.drop_subset(self, col)
                    pu.func_store_col(self.drop_subset, self.func_order)
                    pu.autosave(self.df, self.directory, self.sheet, 
                                self.func_order, enabled=self.auto_save)
                    break
                elif drop_type == ';':
                    self.display_data()
                elif drop_type == '9':
                    break
                elif drop_type == '0':
                    save_check(self.file_directory, self.func_order)
                    sys.exit()
                else:
                    print('Input not recognised, please type again!')
            elif option == '2':
                print(pg.row_col)
                print(pg.back_exit)
                column_row = input('User: ')
                # lets user choose to impute by column or row 
                if column_row == '1': # impute by column
                    print(pg.impute_ops)
                    print(pg.back_exit)
                    impute_option = input('User: ')
                    if impute_option == '1': # impute by mean
                        self.impute_col(self)
                        pu.func_store(self.impute_col, self.func_order)
                        pu.autosave(self.df, self.directory, self.sheet, 
                                    self.func_order, enabled=self.auto_save)
                        break
                    # impute by user defined value on a feature
                    elif impute_option == '2': 
                        col_input = input('Please type in the feature name: ')
                        num_input = input('Please enter a value: ')
                        num = int(num_input)
                        self.impute_num(self, num, col_input)
                        pu.func_store_range(self.impute_num, self.func_order, 2)
                        pu.autosave(self.df, self.directory, self.sheet, 
                                    self.func_order, enabled=self.auto_save)
                    # impute all selected columns by 0
                    elif impute_option == '3':
                        start_col = input('Please type in the starting feature: ')
                        end_col = input('Please type in the ending feature: ')
                        self.impute_zero(self, start_col, end_col)
                        pu.func_store_range(self.impute_zero, self.func_order, 2)
                        pu.autosave(self.df, self.directory, self.sheet,
                                    self.func_order, enabled=self.auto_save)
                        break
                    elif impute_option == ';':
                        self.display_data()
                    elif impute_option == '9':
                        break
                    elif impute_option == '0':
                        sys.exit()
                    else:
                        print('Input not recognised, please type again!')
                elif column_row == '2':
                    self.impute_row(self) # impute by row means
                    pu.func_store(self.impute_row, self.func_order)
                    pu.autosave(self.df, self.directory, self.sheet, 
                                self.func_order, enabled=self.auto_save)
                    break
                elif column_row == ';':
                    self.display_data()
                elif column_row == '9':
                    break
                elif column_row == '0':
                    sys.exit()
                else:
                    print('Input not recognised, please type again!')
            elif option == ';':
                self.display_data()
            elif option == '9':
                break
            elif option == '0':
                save_check(self.file_directory, self.func_order)
                sys.exit()
            else:
                print('Input not recognised, please type again!')
    
    # return the summary statistics table for the data
    def summ_stat(self):
        return self.df.describe()
    
    # check for outliers in the data    
    def outlier_detect(self):
        summary = self.summ_stat()
        for i in range(len(summary.columns)):
            # create a pandas series 
            # for each feature in the summary statistics table
            summ_col = summary.iloc[:, i] 
            # set the outlier range at 3 standard deviations away from the mean
            outlier_range = summ_col.iloc[1] + summ_col.iloc[2]*3 
            col = self.df.iloc[:, i]
            # find the outliers in the column
            out_col = col[np.abs(col) > outlier_range] 
            for j in range(len(out_col)):
                col_name = self.df.columns.values[i] # obtain the feature name
                # store the features and their outlier indexes in a dict
                self.summ[col_name].update({out_col.index[j]: out_col.iloc[j]})
        return self.summ
    
    # checking nans
    def check_na(self):
        na_dict = {}
        # store all features with nans in a list
        for i in range(len(self.df.columns)): 
            na_col = self.df.iloc[:, i]
            check = na_col.hasnans
            if check == True:
                na_dict[self.df.columns.values[i]] = na_col.isna().sum()
        print('Nans check: \n')
        print(na_dict)

# data visualisation class which provide different visualisation options
class DataVisual:
    
    def __init__(self, df=None):
        if df is None:
            df = pd.DataFrame()
        self.df = df
        self.running = True

    def display_data(self):
        print(self.df)
    
    # correlation matrix    
    def corr_matr(self):
        correlation_matrix = self.df.corr().round(1)
        sns.heatmap(data=correlation_matrix, annot=True)
        plt.show(block=False) # show the plot immediately after execution
        
    # bar plot
    def bar_plot(self, feature):
        self.df[feature].plot.bar()
        plt.show(block=False)
        
    # histogram and density plots
    def hist_density_plots(self, feature, no_of_bins):
        print(pg.hist_dens)
        print(pg.back_exit)
        # choose different between data types and plots
        data_type = input('User: ')
        run = True
        while run:
            run = False
            if data_type == '1': # histogram
                sns.distplot(self.df[feature], hist=True, kde=False)
                plt.gca().set(title='Frequency Histogram of {}'.format(feature)
                              , xlabel=feature, ylabel='Frequency')
                plt.show(block=False)
            elif data_type == '2': # density
                sns.distplot(self.df[feature], hist=False, kde = True,
                             kde_kws = {'shade': True, 'linewidth': 3})
                plt.gca().set(title='Density plot of {}'.format(feature),
                              ylabel='Density')
                plt.show(block=False)
            elif data_type == '3': # mixed plot
                sns.distplot(self.df[feature])
                plt.gca().set(title=
                           'Histogram and Density plot of {}'.format(feature),
                           ylabel='Density')
                plt.show(block=False)
            elif data_type == '4': # pairplots
                sns.pairplot(self.df, diag_kind = 'kde', 
                             plot_kws={'alpha': 0.2})
                plt.show(block=False)
            elif data_type == ';':
                self.display_data()
                break
            elif data_type == '9':
                break
            elif data_type == '0':
                sys.exit()
            else:
                print('Input not recognised, please type again!')
                run = True
    
    # scatter regression plot            
    def scatter_plot(self, feature, output):
        print('Scatter regression plot: ')
        sns.regplot(feature, output, data=self.df)
        plt.gca().set(title=
                 'Scatter-Regression plot of {} on {}'.format(feature, output))
        plt.show(block=False)
    
    # visualisation menu                    
    def visualise(self):
        while self.running:
            print(pg.viz)
            print(pg.back_exit)
            option = input('User: ')
            
            if option == '1':
                print('Correlation matrix: \n')
                self.corr_matr()
                break
            elif option == '2':
                feature = input('Please type in the feature name: ')
                try:
                    self.bar_plot(feature)
                except:
                    raise KeyError('cannot find feature')
                break
            elif option == '3': # choose feature and number of bins
                feature = input('Please type in the feature name: ')
                no_of_bins = input('Please type in the number of bins: ')
                try:
                    self.hist_density_plots(feature, no_of_bins)
                except:
                    raise KeyError('cannot find feature')
                break
            elif option == '4': # choose feature and output variable
                feature = input('Please type in the feature name: ')
                output = input('Please type in the output name: ')
                try:
                    self.scatter_plot(feature, output)
                except:
                    raise KeyError('cannot find feature')
                break
            elif option == ';':
                self.display_data()
                break
            elif option == '9':
                break
            elif option == '0':
                sys.exit()
            else:
                print('Input not recognised, please type again!')

class Feature_select:

    def __init__(self, df=None, regressor=None):
        if df is None:
            df = pd.DataFrame()
        self.df = df
        self.y = self.df[regressor]
        self.x = self.df.drop([regressor], axis=1)
        self.running = True

    def display_data(self):
        print(self.df)

    def feature_lasso(self):
        model = LassoCV()
        model.fit(self.x, self.y)
        coefficients = pd.Series(model.coef_, index=self.x.columns)
        print("Beta weights/co-efficients (L1 regularisation)")
        print("-----------------------------------------")
        print(coefficients)
        print('\n')
        print('R2 score is {}'.format(model.score(self.x, self.y)))

    def feature_ridge(self):
        model = RidgeCV()
        model.fit(self.x, self.y)
        coefficients = pd.Series(model.coef_, index=self.x.columns)
        print("Beta weights/co-efficients (L2 regularisation)")
        print("-----------------------------------------")
        print(coefficients)
        print('\n')
        print('R2 score is {}'.format(model.score(self.x, self.y)))

    # feature selection
    def feature_rfe(self, feature_size):
        X_train, X_test, Y_train, Y_test = train_test_split(self.x, self.y, test_size=0.2,
                                                            random_state=5)
        lin_model = LinearRegression()

        rfe = RFE(lin_model, feature_size)
        X_rfe = rfe.fit_transform(X_train, Y_train)
        lin_model.fit(X_rfe, Y_train)
        print(rfe.ranking_)
        print(rfe.support_)

        arr_size = len(self.x.columns)  # finds the total number of columns
        nof_list = np.arange(1, arr_size)
        high_score = 0

        nof = 0
        score_list = []
        for n in range(len(nof_list)):
            rfe = RFE(lin_model, nof_list[n])
            X_train_rfe = rfe.fit_transform(X_train, Y_train)
            X_test_rfe = rfe.transform(X_test)
            lin_model.fit(X_train_rfe, Y_train)
            score = lin_model.score(X_test_rfe, Y_test)
            score_list.append(score)
            if (score > high_score):
                high_score = score
                nof = nof_list[n]

        print('Optimum number of features: %d' % nof)
        print('Score with %d features: %f' % (nof, high_score))

        # find the optimum features to keep
        feature_col = list(self.x)
        fea = pd.Series(rfe.support_, index=feature_col)
        optimum_features = fea[fea == True].index
        print(optimum_features)

    # feature selection menu
    def feature_selection(self):
        while self.running:
            print(pg.feature_sel)
            print(pg.back_exit)
            option = input('User: ')

            if option == '1':
                self.feature_lasso()
                break
            elif option == '2':
                self.feature_ridge()
                break
            elif option == '3':
                user_input = input('Please type in the number of features: ')
                self.feature_rfe(int(user_input))
            elif option == ';':
                self.display_data()
                break
            elif option == '9':
                break
            elif option == '0':
                sys.exit()
            else:
                print('Input not recognised, please type again!')

# save the file directory list to a binary file    
def save_directory(directory_name, fd):
    with open(directory_name, 'w+') as f:
        for item in fd:
            f.write('%s\n' % item)

# save the function order list to a binary file
def save_log(job_history_name, jh):
    with open(job_history_name, 'wb') as f:
        dill.dump(jh, f)

# asks if the user wants to save the directory information 
# and job history (function call order)
def save_check(fd, jh):
    user_input = input(pg.save_log)
    if user_input == 'yes':
        directory_name = input(pg.save_direc)
        job_history_name = input(pg.save_job)
        # the lists containing class methods and dictionaries 
        # are stored in a .pkl file
        combine_suffix_d = (directory_name, '.txt')
        combine_suffix_j = (job_history_name, '.pkl')
        direc = ''.join(combine_suffix_d)
        jobh = ''.join(combine_suffix_j)
        save_directory(direc, fd)
        save_log(jobh, jh)
        print('file saved!')
    else:
        pass