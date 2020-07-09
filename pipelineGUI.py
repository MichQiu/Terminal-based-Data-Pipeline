'''Data pipeline GUI displays'''

'''
This file contains the GUI displays for all the pages within the user
terminal.
'''

# feature operation options
feature_ops = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##          Reduction           ##    ##         Normalisation        ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
  
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##        Transformation        ##    ##            Rename            ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 3                                Press 4                             

                      ##################################
                      ##                              ##
                      ##        Label encoding        ##
                      ##                              ##
                      ##################################
                                    Press 5 

'''

rename_type = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##        Single feature        ##    ##       Multiple features      ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
'''

# feature normalisation options
feature_norm = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##           Z score            ##    ##            Min-max           ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
'''

# feature transformaton options
feature_trans = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##             Mean             ##    ##      Interquartile range     ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
  
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##      Percentage to whole     ##    ##      Whole to percentage     ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 3                                Press 4                                
'''

# drop/impute nans options
drop_imp = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##             Drop             ##    ##            Impute            ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
'''

# drop all or subset options
all_subset = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##             All              ##    ##            Subset            ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
'''

# impute by row or column options
row_col = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##            Column            ##    ##              Row             ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
'''

impute_ops = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##             Mean             ##    ##      User defined value      ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
                
                      ##################################
                      ##                              ##
                      ##             Zero             ##
                      ##                              ##
                      ##################################
                                    Press 3  
'''

# other options
back_exit = '''
                          ##########################       
                          ##                      ##      
                          ##     Display data     ##       
                          ##                      ##       
                          ##########################       
                                    Press ; 

          ##########################       ##########################    
          ##                      ##       ##                      ##
          ##         Back         ##       ##         Exit         ##
          ##                      ##       ##                      ##
          ##########################       ##########################
                   Press 9                           Press 0 

===============================================================================
'''

# data visualisation options
viz = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##      Correlation matrix      ##    ##           Bar plot           ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
  
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##  Histogram and Density plot  ##    ##         Scatter plot         ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 3                                Press 4
'''

# histogram/density plot options
hist_dens = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##           Discrete           ##    ##           Continous          ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
  
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##            Mixed             ##    ##          Paired plot         ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 3                                Press 4
'''

# linespace template   
linespace = '''
===============================================================================
'''

# title template
title = '''
               ###############################################
               #######                                 #######
               #######   Data preparation pipelne-v1   #######
               #######                                 #######
               ###############################################
        
===============================================================================
'''

# data function options
function_selection = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##  Data cleaning/engineering   ##    ##      Data visualisation      ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
   
   ##################################    ##################################
   ##                              ##    ##                              ##
   ##       Feature selection      ##    ##          Export data         ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 3                                Press 4

                      ##################################
                      ##                              ##
                      ##             Exit             ##
                      ##                              ##
                      ##################################
                                    Press 0 
                                    
===============================================================================
'''

# data cleaning/engineering template
dc = '''
               ###############################################
               #######                                 #######
               #######    Data cleaning/engineering    #######
               #######                                 #######
               ###############################################
               
===============================================================================
'''

# data visualisation template
dv = '''
               ###############################################
               #######                                 #######
               #######       Data visualisation        #######
               #######                                 #######
               ###############################################

===============================================================================
'''

# other function template    
fs = '''
               ###############################################
               #######                                 #######
               #######        Feature selection        #######
               #######                                 #######
               ###############################################

===============================================================================
'''

# other options
option = '''
                         ##########################       
                         ##                      ##      
                         ##     Display data     ##       
                         ##                      ##       
                         ##########################       
                                   Press ; 

         ##########################       ##########################    
         ##                      ##       ##                      ##
         ##      Clear data      ##       ##         Back         ##
         ##                      ##       ##                      ##
         ##########################       ##########################
                  Press 7                           Press 8
                
         ##########################       ##########################    
         ##                      ##       ##                      ##
         ##       Main menu      ##       ##         Exit         ##
         ##                      ##       ##                      ##
         ##########################       ##########################
                  Press 9                           Press 0 

===============================================================================
'''

# data cleaning/engineering options
data_ops = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##    Missing data operations   ##    ##      Feature operations      ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
  
                      ##################################
                      ##                              ##
                      ##      Summary statistics      ##
                      ##                              ##
                      ##################################
                                    Press 3                                    
'''

# missing data operations options
missing_data = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##  Check missing values (nans) ##    ##        Drop and impute       ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
'''

# summary statistics options         
summ_stat_ops = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##   Summary statistics table   ##    ##       Outlier detection      ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2
'''

# feature selection options
feature_sel = '''
   ##################################    ##################################    
   ##                              ##    ##                              ##
   ##            Lasso             ##    ##             Ridge            ##
   ##                              ##    ##                              ##
   ##################################    ##################################
                Press 1                                Press 2

                      ###################################
                      ##                               ##
                      ## Recursive feature elimination ##
                      ##                               ##
                      ###################################
                                    Press 3                                    
'''

data_directory = '''
Please type in the directory of where your data is located: 
'''

data_sheet = '''Please type in the sheet name of the data file: '''

feature_rename = '''Please type in the features you wish to rename: '''

range_option = '''Do you want to conduct operations by individual features or by range? Please type 1 for individual and 2 for range: '''

select_fin = '''Please type * when you have finished typing in all your selected features'''

select_fea = '''Please type in the features you wish to select: '''

feature_repeat = '''Do you still want to conduct feature operations? Type yes or no: '''

save_log = '''Do you wish to save the directory and function calls to the log files? Type yes or no '''

save_direc = '''Please type in the filename for storing the directory information: '''

save_job = '''Please type in the filename for storing function call information: '''

data_direc_import = '''Please type in the location of the directory file: '''

job_hist_import = '''Please type in the location of the job history file: '''

data_loc = '''Please type in the location where you would like to save the file: '''

list_d = '''Please type in the name of the feature names file: '''