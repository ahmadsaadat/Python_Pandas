import sys
sys.path.insert(0, '../')

import pytest
import pandas as pd
from src import main


def test_operation_number_of_distinct_ETFs_per_day_1():
    input_directory = './data/input_raw/'
    output_directory = './data/output/'
    build_df = main.IO_build_df(input_directory)
    result_df = main.operation_number_of_distinct_ETFs_per_day_1(build_df)
    
    # check to see if return type of build_df is dataframe
    assert isinstance(build_df, pd.DataFrame)
    # check to see if return type of result_df is dataframe
    assert isinstance(result_df, pd.DataFrame)
    
    test_df = pd.DataFrame(
    [[1, 4], 
     [2, 3]],
    columns=['Day', 'Distinct ETFs per Day']
    )
    
    
    # check to see if the shape of return result_df df is 2x2
    assert result_df.shape == (2, 2)
    # check to see if the calculation was correct
    pd.testing.assert_frame_equal(result_df, test_df)
    
    # export csv
    main.IO_output_to_csv(output_directory+'1_number_of_distinct_ETFs_per_day.csv', result_df)

    
    
def test_operation_number_of_constituents_per_ETF_2():
    input_directory = './data/input_raw/'
    output_directory = './data/output/'
    build_df = main.IO_build_df(input_directory)
    result_df = main.operation_number_of_constituents_per_ETF_2(build_df)
    
    # check to see if return type of build_df is dataframe
    assert isinstance(build_df, pd.DataFrame)
    # check to see if return type of result_df is dataframe
    assert isinstance(result_df, pd.DataFrame)
    
    test_df = pd.DataFrame(
    [
        [1, 'ETF1', 4], 
        [1, 'ETF2', 3], 
        [1, 'ETF3', 3], 
        [1, 'ETF4', 3], 
        [2, 'ETF1', 3], 
        [2, 'ETF2', 3], 
        [2, 'ETF3', 3], 
    ],
    columns=['Day', 'Composite AxiomaID', 'Number of constituents']
    )
    
    # check to see if the shape of return result_df df is 2x2
    assert result_df.shape == (7, 3)
    # check to see if the calculation was correct
    pd.testing.assert_frame_equal(result_df, test_df)
    
    # export to csv
    main.IO_output_to_csv(output_directory+'2_number_of_constituents_per_ETF_per_Day.csv', result_df)


def test_operation_dropped_and_added_constituents_per_timeframe_3():
    input_directory = './data/input_raw/'
    output_directory = './data/output/'
    build_df = main.IO_build_df(input_directory)
    result_df = main.operation_dropped_and_added_constituents_per_timeframe_3(build_df)
    
    # pull out the two dfs from list
    dropped_df = result_df[0]
    added_df = result_df[1]
    
    # check to see if return type of build_df is dataframe
    assert isinstance(build_df, pd.DataFrame)
    # check to see if return type of result_df is list
    assert isinstance(result_df, list)
    # check to see if contents are of type DataFrame
    assert isinstance(dropped_df, pd.DataFrame)
    assert isinstance(added_df, pd.DataFrame)
    
    mock_dropped_df = pd.DataFrame(
    [
        ['AAPL'],
        ['MA']
    ],
    columns=['Constituents dropped from Day2']
    )
    
    mock_added_df = pd.DataFrame(
    [
        ['HD']
    ],
    columns=['Constituents added to Day2']
    )
    
    # check to see if the dropped_df is 2x1
    assert dropped_df.shape == (2, 1)
    # check to see if the dropped constituents was correct
    pd.testing.assert_frame_equal(dropped_df, mock_dropped_df)
    
    # check to see if the added_df is 1x1
    assert added_df.shape == (1, 1)
    # check to see if the added constituents was correct
    pd.testing.assert_frame_equal(added_df, mock_added_df)
    
    # export to CSV
    main.IO_output_to_csv(output_directory+'3_0_dropped_constituents_between_Day1_and_Day2.csv', dropped_df)
    main.IO_output_to_csv(output_directory+'3_1_added_constituents_between_Day1_and_Day2.csv', added_df)
    
    
    
def test_operation_max_constituent_weight_change_per_ETF_4():
    # For each ETF, indicate which constituent’s weight has changed the MOST from DAY1 to DAY2
    input_directory = './data/input_raw/'
    output_directory = './data/output/'
    build_df = main.IO_build_df(input_directory)
    result_df = main.operation_max_constituent_weight_change_per_ETF_4(build_df)
    
    test_df = pd.DataFrame(
    [
        ['ETF1', 'TSLA', 0.2500, 0.30, 20.000000],
        ['ETF2', 'MSFT',  0.3333, 0.40, 20.012001],
        ['ETF3', 'V',  0.1000, 0.15, 50.000000]
    ],
    columns=['Composite AxiomaID', 'Constituent AxiomaID', 'Weight Day1', 'Weight Day2', 'pct_change']
    )
    
    # check to see if return type of build_df is dataframe
    assert isinstance(build_df, pd.DataFrame)
    # check to see if return type of result_df is list
    assert isinstance(result_df, pd.DataFrame)
    
    # check to see if the added_df is 3x5
    assert result_df.shape == (3, 5)
    # check to see if percentage change per ETF and constituents is correct
    pd.testing.assert_frame_equal(result_df, test_df)
    
    # export to csv
    main.IO_output_to_csv(output_directory+'4_max_constituent_percentage_change_per_ETF.csv', result_df)
    
    
if __name__== "__main__":
    test_operation_number_of_distinct_ETFs_per_day_1()
    test_operation_number_of_constituents_per_ETF_2()
    test_operation_dropped_and_added_constituents_per_timeframe_3()
    test_operation_max_constituent_weight_change_per_ETF_4()