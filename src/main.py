import pandas as pd
import os
import csv

def IO_build_df(directory):
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
    

def operation_number_of_distinct_ETFs_per_day_1(df):
# For each DAY (DAY1 and DAY2), indicate how many distinct ETFs are present
    distinct_etf_df = df.groupby(['Day'])
    distinct_etf_df = distinct_etf_df['Composite AxiomaID'].nunique().to_frame()
    distinct_etf_df = distinct_etf_df.reset_index(inplace=False)
    
    # beautify return df
    distinct_etf_df = distinct_etf_df.rename(columns={'Composite AxiomaID': 'Distinct ETFs per Day'})
    return distinct_etf_df

def operation_number_of_constituents_per_ETF_2(df):
# For each DAY, for each ETF provide a breakdown of how many constituents are present in each ETF
    groupby_constituent_df = df.groupby(['Day', 'Composite AxiomaID'])
    groupby_constituent_df = groupby_constituent_df['Constituent AxiomaID'].size().to_frame()
    groupby_constituent_df = groupby_constituent_df.reset_index(inplace=False)
    return groupby_constituent_df

def operation_dropped_and_added_constituents_per_timeframe_3(df):
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
    
def operation_max_constituent_weight_change_per_ETF_4(df):
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

def IO_output_to_csv(directory, df):
    df.index.name = "Index"
    df.to_csv(directory, sep='|', encoding='utf-8')
    

if __name__== "__main__":
    input_directory = './data/input_raw/'
    output_directory = './data/output/'
    
    # build dataframe consisting of day1 and day2 data
    build_df = IO_build_df(input_directory)
    IO_output_to_csv(output_directory+'0_build_df.csv', build_df)
    
    # 1: For each DAY (DAY1 and DAY2), indicate how many distinct ETFs are present
    df_1 = operation_number_of_distinct_ETFs_per_day_1(build_df)
    IO_output_to_csv(output_directory+'1_number_of_distinct_ETFs_per_day.csv', df_1)
    
    # 2: For each DAY, for each ETF provide a breakdown of how many constituents are present in each ETF
    df_2 = operation_number_of_constituents_per_ETF_2(build_df)
    IO_output_to_csv(output_directory+'2_number_of_constituents_per_ETF_per_Day.csv', df_2)
    
    # 3: Between DAY 1 and DAY 2, which constituent has been dropped and which has been added
    df_3 = operation_dropped_and_added_constituents_per_timeframe_3(build_df)
    # TODO: in the output you'll see weight, what does this mean?
    IO_output_to_csv(output_directory+'3_0_dropped_constituents_between_Day1_and_Day2.csv', df_3[0])
    IO_output_to_csv(output_directory+'3_1_added_constituents_between_Day1_and_Day2.csv', df_3[1])
    
    # 4: Max constituent percentage change, per ETF
    df_4 = operation_max_constituent_weight_change_per_ETF_4(build_df)
    IO_output_to_csv(output_directory+'4_max_constituent_percentage_change_per_ETF.csv', df_4) 
    

    
