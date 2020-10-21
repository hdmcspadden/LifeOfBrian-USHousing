# -*- coding: utf-8 -*-
import unittest

import pandas as pd

from common_functions_Class import COMMONFUNCTIONS

# Class for testing BOOKLOVER classes.
class CommonFunctionsTestClass(unittest.TestCase): # inherit from unittest.TestCase
    

    def setUp(self):
        # test GDP dataframe to use for test calculations
        self.dfGDP = pd.DataFrame([[1995, 2001, 1000], [2007, 2010, 1000]], columns=['year', 'current dollars', 'GDP'])
        
    
   
    def test_correctInflationAdjustmentFrom1995(self):
        # create the COMMONFUNCTIONS class       
        cf = COMMONFUNCTIONS()
        
        dfInflation = cf.inflation_adjust(self.dfGDP)
        
         # correct calculation of 1995 dollars entered as 1000 dollars in 2001 dollars is 1148
        self.assertEqual(int(dfInflation["inf-adjusted"][0]), 1448)   

        
    def test_correctInflationAdjustmentFrom2007(self):
        
        # create the COMMONFUNCTIONS class       
        cf = COMMONFUNCTIONS()
              
        
        dfInflation = cf.inflation_adjust(self.dfGDP)
        
        # correct calculation of 2007 dollars entered as 1000 dollars in 2010 dollars is 1175
        self.assertEqual(int(dfInflation["inf-adjusted"][1]), 1175)   

if __name__ == '__main__':
    unittest.main() 
        
        
        

