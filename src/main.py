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

def calculate_compare_days_difference_3(df):
# Compare DAY1 to DAY2.  For a given ETF, indicate which constituent has dropped from DAY1 to 
# DAY2, and which constituent has been added from DAY1 to DAY2

    day1_dataframe = df[df['Day'] == 1]
    # day1_dataframe = day1_dataframe[day1_dataframe['Composite AxiomaID'] == 'ETF4']
    day2_dataframe = df[df['Day'] == 2]
    # day2_dataframe = day2_dataframe[day2_dataframe['Composite AxiomaID'] == 'ETF4']
    
    # do a left join to find out what rows are only in Day1 and not in Day2
    left_join_dataframes = pd.merge(day1_dataframe, day2_dataframe, how='left', on=["Composite AxiomaID", "Constituent AxiomaID"], suffixes=['_day1', '_day2'])
    # keep only dropped constituents per ETF
    dropped_dataframes = left_join_dataframes[(left_join_dataframes['Weight_day2'].isnull()) & (left_join_dataframes['Day_day2'].isnull())]
    dropped_dataframes = dropped_dataframes.drop(['Weight_day2', 'Day_day2'], axis=1)
    dropped_dataframes = dropped_dataframes.rename(columns={'Weight_day1': 'Weight', 'Day_day1':'Day'})
    
    # do a right join to find out what rows are only in Day2 and not in Day1
    right_join_dataframes = pd.merge(day1_dataframe, day2_dataframe, how='right', on=["Composite AxiomaID", "Constituent AxiomaID"], suffixes=['_day1', '_day2'])
    added_dataframes = right_join_dataframes[(right_join_dataframes['Weight_day1'].isnull()) & (right_join_dataframes['Day_day1'].isnull())]
    added_dataframes = added_dataframes.drop(['Weight_day1', 'Day_day1'], axis=1)
    added_dataframes = added_dataframes.rename(columns={'Weight_day2': 'Weight', 'Day_day2':'Day'})
    
    #reset indexes
    dropped_dataframes = dropped_dataframes.reset_index(inplace=False)
    added_dataframes = added_dataframes.reset_index(inplace=False)
    
    #reposition column indexes
    reposition_cols = ["Day","Composite AxiomaID","Constituent AxiomaID","Weight"]
    dropped_dataframes = dropped_dataframes.reindex(columns=reposition_cols)
    added_dataframes = added_dataframes.reindex(columns=reposition_cols)

    #return a list, the former containing dropped constituents per ETF, and the latter containing added constituents per ETF
    return [dropped_dataframes, added_dataframes]
    
def calculate_percentage_change_per_constituent_4(df):
    # For each ETF, indicate which constituent’s weight has changed the MOST from DAY1 to DAY2

    day1_dataframe = df[df['Day'] == 1]
    day1_dataframe = day1_dataframe.rename(columns={'Weight' : 'Weight Day1'})
    # print(day1_dataframe)

    day2_dataframe = df[df['Day'] == 2]
    day2_dataframe = day2_dataframe.rename(columns={'Weight' : 'Weight Day2'})
    # print(day2_dataframe)

    combined_dfs = pd.merge(day1_dataframe, day2_dataframe, on=['Composite AxiomaID','Constituent AxiomaID'], how='inner')
    combined_dfs = combined_dfs.drop(['Day_x', 'Day_y'], axis=1)

    combined_dfs['pct_change'] = ((combined_dfs['Weight Day2'] - combined_dfs['Weight Day1']) / combined_dfs['Weight Day1']) * 100
    
    combined_dfs = combined_dfs.sort_values(by='pct_change', axis=0, inplace=False, ascending=False)
    
    # group by and find max pct_change per ETF, return dataframe
    # combined_dfs = combined_dfs.groupby(['Composite AxiomaID'])['pct_change'].max().to_frame()
    
    # instead of doing group by trying getting a series
    max_index_series = combined_dfs.groupby(['Composite AxiomaID'])['pct_change'].idxmax()
    combined_dfs = combined_dfs.loc[max_index_series]
    
    #reset and recalibrate indexes
    combined_dfs = combined_dfs.reset_index(inplace=False, drop=True)
    
    return combined_dfs

if __name__== "__main__":
    directory = './data/input_raw/'
    # get a combined dataframe consisting of day1 and day2 data
    df = build_df(directory)
    #1: For each DAY (DAY1 and DAY2), indicate how many distinct ETFs are present
    distinct_ETFs_result = calculate_distinct_ETFs_1(df)
    print(distinct_ETFs_result)

    
