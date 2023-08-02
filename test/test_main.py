import sys
sys.path.insert(0, '../')

import pytest
import pandas as pd
from src import main


def test_calculate_distinct_ETFs_1():
    directory = './data/input_raw/'
    build_df = main.build_df(directory)
    result_df = main.calculate_distinct_ETFs_1(build_df)
    
    # check to see if return type of build_df is dataframe
    assert isinstance(build_df, pd.DataFrame)
    # check to see if return type of result_df is dataframe
    assert isinstance(result_df, pd.DataFrame)
    
    print(result_df)
    
    test_df = pd.DataFrame(
    [[1, 4], 
     [2, 3]],
    columns=['Day', 'Composite AxiomaID']
    )
    
    # check to see if the shape of return result_df df is 2x2
    assert result_df.shape == (2, 2)
    # check to see if the calculation was correct
    pd.testing.assert_frame_equal(result_df, test_df)
    
def test_calculate_groupby_constituents_2():
    directory = './data/input_raw/'
    build_df = main.build_df(directory)
    result_df = main.calculate_groupby_constituents_2(build_df)
    
    # check to see if return type of build_df is dataframe
    assert isinstance(build_df, pd.DataFrame)
    # check to see if return type of result_df is dataframe
    assert isinstance(result_df, pd.DataFrame)
    
    print(result_df)
    
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
    columns=['Day', 'Composite AxiomaID', 'Constituent AxiomaID']
    )
    
    # check to see if the shape of return result_df df is 2x2
    assert result_df.shape == (7, 3)
    # check to see if the calculation was correct
    pd.testing.assert_frame_equal(result_df, test_df)
    
    
    
if __name__== "__main__":
    test_calculate_distinct_ETFs_1()
    test_calculate_groupby_constituents_2()