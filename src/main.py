import pandas as pd
import os
import csv

# get a list of all the raw files in input_raw directory
directory = '../data/input_raw/'
file_list = os.listdir(directory)

#declare combined dataframe to hold day 1 and day 2 records
df = pd.DataFrame()

# for every file that exists in input_raw directory
# slice, dice and extract information from first two rows
# then create appropriate dataframes
# and finally merge data frames into main df declared above
for file_name in file_list:
    file_directory = directory + file_name
    with open(file_directory, 'r') as f:
        date_line = f.readline().strip()
        extract_day = date_line.split('#DataDate: DAY')[1]
        
        columns_line = f.readline().strip()
        extract_columns = columns_line.split('#Columns: ')[1]
        columns_list = extract_columns.split('|')
        
        file_df = pd.read_csv('../data/input_raw/DAY1.txt', sep='|', skiprows=2)
        file_df.columns = columns_list
        file_df['Day'] = int(extract_day)
        
        df = pd.concat([df, file_df])
    



# df.to_csv('file_name.csv', encoding='utf-8', index=False)

    
