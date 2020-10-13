# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 22:07:53 2020

@author: Katie
"""

import unittest
from gdpPDFCleaning import *
import pandas as pd

#%%

class YearlyGDPTestCase(unittest.TestCase):
    
    def test_dataframeConstructor_creates_blank_dataframe(self):
        # test that the constructor correctly creates a blank DataFrame
        # when no DataFrame is passed
        
        # Set Up
        df1 = YearlyGDP('testPDF.pdf', 1, 1995, 1998)
        actual = df1.df
        expected = pd.DataFrame()    
        
        # Test
        pd.testing.assert_frame_equal(actual, expected)
        
    def test_dataframeConstructor_assigns_dataframe(self):
        # test that the constructor assigns the DataFrame passed correctly
        
        # Set Up
        data = pd.DataFrame({'Name': ['Bob', 'Sue', 'Mary'], 'Age': [21, 22, 23]})
        df1 = YearlyGDP('testPDF.pdf', 1, 1995, 1998, data)
        actual = df1.df
        expected = data
        
        # Test
        pd.testing.assert_frame_equal(actual, expected)
        
        
    def test_initialize_DataFrame_columnNameChange(self):
        # test that the changeColumnNames function is pulling the names
        # from the first row of the DataFrame into an assigned variable
        
        # Set Up
        df1 = YearlyGDP('testPDF.pdf', 1, 1995, 1998)
        df1.initializeDataFrame()
        
        actual = df1.df.columns
        expected = pd.Series(['Column1','Column2','Column3', 'Column4'])
        
        # Test
        self.assertEqual(actual.all(), expected.all())
    
#%%
        
if __name__ == '__main__':
    log_file = 'gdpPDFCleaning Test Output.txt'
    with open(log_file, 'w') as f:
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)