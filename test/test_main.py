import sys
sys.path.insert(0, '../')

import pytest
import pandas as pd
from src import main

def test_distinct_etfs_1():
    directory = './data/input_raw/'
    build_df = main.build_df(directory)
    result_df = main.calculate_distinct_ETFs_1(build_df)
    
    # check to see if return type of build_df is dataframe
    assert isinstance(build_df, pd.DataFrame)
    # check to see if return type of result_df is dataframe
    assert isinstance(result_df, pd.DataFrame)
    
    test_df = pd.DataFrame(
    [[1, 4], 
     [2, 3]],
    columns=['Day', 'Composite AxiomaID']
    )
    
    # check to see if the shape of return result_df df is 2x2
    assert result_df.shape == (2, 2)
    # check to see if the calculation was correct
    pd.testing.assert_frame_equal(result_df, test_df)
    
    
if __name__== "__main__":
    test_distinct_etfs_1()