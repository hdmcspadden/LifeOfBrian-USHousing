# -*- coding: utf-8 -*-
import unittest

import pandas as pd

from common_functions_Class import COMMONFUNCTIONS

# Class for testing BOOKLOVER classes.
class CommonFunctionsTestClass(unittest.TestCase): # inherit from unittest.TestCase
    

    # use setup() to define fixtures to use for testing in the unit tests
    def setUp(self):
        # test GDP dataframe to use for test calculations
        self.dfGDP = pd.DataFrame([[1995, 2001, 1000], [2007, 2010, 1000]], columns=['year', 'current dollars', 'GDP'])
        
        # dataframe with value and dollar-yr for use in testing inflation_adjust_to2019
        self.dfDollarsYears = pd.DataFrame([[100,"2017"],[100,"2018"],[100,"2019"]], columns=['value','dollar-yr'])
        
        # price dictionary with known Constant Multiplier for each year
        self.price_dict = {"2017":0.95833, "2018":.98214, "2019": 1}
    
   
    def test_correctInflationAdjustmentFrom1995(self):
        # create the COMMONFUNCTIONS class       
        cf = COMMONFUNCTIONS()
        
        # call the function with the dfGDP fixture
        dfInflation = cf.inflation_adjust(self.dfGDP)
        
         # correct calculation of 1995 dollars entered as 1000 dollars in 2001 dollars is 1148
        self.assertEqual(int(dfInflation["inf-adjusted"][0]), 1448)   

        
    def test_correctInflationAdjustmentFrom2007(self):
        
        # create the COMMONFUNCTIONS class       
        cf = COMMONFUNCTIONS()
              
        # call the function with the dfGDP fixture
        dfInflation = cf.inflation_adjust(self.dfGDP)
        
        # correct calculation of 2007 dollars entered as 1000 dollars in 2010 dollars is 1175
        self.assertEqual(int(dfInflation["inf-adjusted"][1]), 1175)   
    
    def test_inflation_adjust_to2019(self): 
        
        cf = COMMONFUNCTIONS()
        
        # run the inflation adject to 2019 dollars function
        dfAdjusted = cf.inflation_adjust_to2019(self.dfDollarsYears, self.price_dict)
        
        # We expect 2017 to be $104, 2018 to be $102, and 2019 to be $100
        self.assertEqual(str(int(dfAdjusted["inf-adjusted"][0])) + " " + str(int(dfAdjusted["inf-adjusted"][1])) + " " + str(int(dfAdjusted["inf-adjusted"][2])), "104 102 100")  

if __name__ == '__main__':
    unittest.main() 
        
        
        

