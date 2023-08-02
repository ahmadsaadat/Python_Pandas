import pandas as pd
import os
import csv


def build_df(directory):
    # get a list of all the raw files in input_raw directory
    file_list = os.listdir(directory)

    #declare combined dataframe to hold day 1 and day 2 records
    df = pd.DataFrame()

    # for every file that exists in input_raw directory
    # slice, dice and extract information from first two rows
    # then create appropriate dataframes
    # and finally merge data frames into a combined df 
    for file_name in file_list:
        file_directory = directory + file_name
        with open(file_directory, 'r') as f:
            date_line = f.readline().strip()
            extract_day = date_line.split('#DataDate: DAY')[1]
            
            columns_line = f.readline().strip()
            extract_columns = columns_line.split('#Columns: ')[1]
            columns_list = extract_columns.split('|')
            
            #skip first two rows
            file_df = pd.read_csv(directory+file_name, sep='|', skiprows=2, header=None)
            #drop last row
            file_df = file_df.iloc[:-1]
            #add the appropriate columns
            file_df.columns = columns_list
            #add the day as a row that pertains to the ETF data collected that day
            file_df['Day'] = int(extract_day)
            df = pd.concat([df, file_df])
    #return combined day1 and day2 df    
    return df
    

def calculate_distinct_ETFs_1(df):
# For each DAY (DAY1 and DAY2), indicate how many distinct ETFs are present
    distinct_etf_df = df.groupby(['Day'])
    distinct_etf_df = distinct_etf_df['Composite AxiomaID'].nunique().to_frame()
    distinct_etf_df = distinct_etf_df.reset_index(inplace=False)
    return distinct_etf_df

def calculate_groupby_constituents_2(df):
# For each DAY, for each ETF provide a breakdown of how many constituents are present in each ETF
    groupby_constituent_df = df.groupby(['Day', 'Composite AxiomaID'])
    groupby_constituent_df = groupby_constituent_df['Constituent AxiomaID'].size().to_frame()
    groupby_constituent_df = groupby_constituent_df.reset_index(inplace=False)
    return groupby_constituent_df

    

if __name__== "__main__":
    directory = './data/input_raw/'
    # get a combined dataframe consisting of day1 and day2 data
    df = build_df(directory)
    #1: For each DAY (DAY1 and DAY2), indicate how many distinct ETFs are present
    distinct_ETFs_result = calculate_distinct_ETFs_1(df)
    print(distinct_ETFs_result)

    
