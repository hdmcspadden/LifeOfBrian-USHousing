# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 22:07:49 2020

@author: Katie
"""

import tabula
import pandas as pd
import re
import math

#%%

class YearlyGDP():
    
# =============================================================================
#     Variables needed for YearlyGDP():
#       -File Name: to read in the PDF
#       -Page Number: page where the GDP table is (in current dollars)
#       -yearStart: the first year of data you want pulled from the table
#       -yearEnd: the last year of data you want pulled from the table (do not
#                 choose the year that is estimated, usually the last year)
#       -dollars: current year dollars that the numbers are in
#       -df: optional; only meant to initialize a df instance for the class
#            object that can be edited by instance
# =============================================================================
    
    
    def __init__(self, file, pageNum, yearStart, yearEnd, dollars, df = pd.DataFrame()):
        self.file = file
        self.pageNum = pageNum
        self.yearStart = yearStart
        self.yearEnd = yearEnd
        self.dollars = dollars
        self.df = df
    
    
    # function to initialize the DataFrame by reading the PDF and updating
    # the column names
    def initializeDataFrame(self):
        # read the PDF and assign the first DataFrame in the list as the
        # self.df; for GDP PDF's, there is only one table per page so this
        # is fine for this application
        
        list_df = tabula.read_pdf(self.file, pages = self.pageNum, stream = True)
        self.df = list_df[0]
        
        # make sure the first row of the DataFrame (which has the real column
        # names) is in str format for regular expression (re)
        self.df.iloc[0].apply(str)
        
        # for loop that indexes by the number of columns
        for i in range(len(self.df.columns)):
            # looking only in the first row, is the ith column a string number?
            # using try/except because the NaN values will throw an AttributeError
            # since NaN is float type and float type does not have attribute
            # isnumeric()
            try:
                if self.df.iloc[0,i].isnumeric():
                    pass
                else:
                    # using re to remove the revision and proposed estimate
                    # symbols from the column names so that we can iterate
                    # through the numbers
                    self.df.iloc[0, i] = re.sub("[\/a-zA-Z*]",'', self.df.iloc[0, i])
            except AttributeError:
                # if the value is not a string (NaN, float type), test if it
                # is an integer; if it is, pass
                if self.df.iloc[0,i].is_integer():
                    pass
                
                # if it is not an interger (NaN), then ideally we would want
                # to rename is to a different string for editing later
                else:
                    pass
        
        # the first column is always area (state, summary levels, etc.)
        # rename that value prior to pulling the column names (much easier)
        self.df.iloc[0,0] = 'Area'
        
        # pull the Series for the first row of DataFrame (contains the true
        # column names)
        name = self.df.loc[0,]
        
        # assign new column names, drop the first row, and reset the index
        # back to 0 for ease of use later
        self.df = self.df.rename(columns = name).drop(self.df.index[0]).reset_index(drop = True)
        
        # return the DataFrame for viewing to ensure changes were made as expected
        return self.df
        
    
    def cleanStates(self, columnName = 'Area'):
        # default name for the states column is 'Area' based on the
        # intializeDataFrame function and for consistency
        
        # make sure the column specified is string type
        if self.df[columnName].dtype == 'str':
            # if string type already, pass
            pass
        else:
            # change column to string type if not already
            self.df[columnName] = self.df[columnName].astype('str')
        
        # clean the white space and periods from the area column
            
        # create a list to hold the cleaned area names
        clean_areas = []
        
        # for every index in the column
        for i in self.df[columnName].index:
            try:
                # check to see if it is NaN
                if math.isnan(self.df.loc[i, columnName]):
                    # don't need to do anything to NaN values
                    pass
                else:
                    # assign the string to the area variable
                    area = self.df.loc[i, columnName]
                    #clean out periods and white space using re
                    clean_areas.append(' '.join(re.sub("[\s\.\/0-9*]"," ", area).split()))
            except TypeError:
                # if a string is fed into the math.isnan() function, it throws
                # a type error; since string is what we want, we just do the re
                
                # assign the string to the area variable
                area = self.df.loc[i, columnName]
                #clean out periods and white space using re
                clean_areas.append(' '.join(re.sub("[\s\.\/0-9*]"," ", area).split()))
            
        # Loop through the list to add the cleaned areas back into the DataFrame
        # using loc() method
                
        # the clean_areas list has the same index as the 'Area' column, so
        # the corresponding cleaned name will end up in the same row
        for i in self.df[columnName].index:
            try:
                # again, we want to ignore NaN values
                if math.isnan(self.df.loc[i, columnName]):
                    pass
                else:
                    # if not NaN, the add the associated clean_area index value
                    self.df.loc[i , f'Cleaned {columnName}'] = clean_areas[i]
            except TypeError:
                # a TypeError is thrown if a string is passed to the math.isnan()
                # method; since a string (or floar) is what we want, we continue
                # with the action
                self.df.loc[i , f'Cleaned {columnName}'] = clean_areas[i]
        
        # return DataFrame to ensure cleaned state names appear as expected
        return self.df
    
    
    def addGeoLocColumn(self, columnNameofStates = 'Cleaned Area'):
# =============================================================================
#         Method to add a Geo Loc tag to each entry (except for the summary lines)
#         summary lines are excluded since that can be calculated by querying
#         by Geo Loc
#           -columnNameofStates: optional; only change if user did not name
#                                the column conventionally
# =============================================================================
        
        # summary categories are the same throughout GDP files
        summary = ['United States', 'New England', 'Mideast', 'Great Lakes',
           'Plains', 'Southeast', 'Southwest', 'Rocky Mountain', 'Far West']
        
        # list created to hold the Geo Loc's found within the table (should be
        # all of them, but just in case)
        geoLoc_list = []
        
        # list to hold the DataFrame row index for the summary line (all the rows)
        # after that index and before the next index are a part of that summary
        # level
        index_list = []
        
        # for all of the rows in the clean_area column
        for i in self.df[columnNameofStates].index:
            try:
                # again, ignore NaN
                if math.isnan(self.df.loc[i, columnNameofStates]):
                    pass
                else:
                    # if not NaN, test to see if it is in the summary (thereby
                    # ignoring the staes)
                    if self.df.loc[i, columnNameofStates] in summary:
                        # if in the summary, add summary name to geoLoc_list
                        geoLoc_list.append(self.df.loc[i, columnNameofStates])
                        # if in the summary, add index of summary name to index_list
                        index_list.append(i)
            except TypeError:
                # a TypeError is thrown if a string is passed to the math.isnan()
                # method
                if self.df.loc[i, columnNameofStates] in summary:
                        # if in the summary, add summary name to geoLoc_list
                        geoLoc_list.append(self.df.loc[i, columnNameofStates])
                        # if in the summary, add index of summary name to index_list
                        index_list.append(i)
                        
                        
        # adding Geo Loc tags for the first geoLoc (not include US total)
        for i in range(index_list[1]+1, index_list[2]):
            self.df.loc[i, 'Geo Loc'] = geoLoc_list[1]
        
        # adding Geo Loc tags for the second geoLoc (not include US total
        for i in range(index_list[2]+1, index_list[3]):
            self.df.loc[i, 'Geo Loc'] = geoLoc_list[2]
        
        # adding Geo Loc tags for the third geoLoc (not include US total
        for i in range(index_list[3]+1, index_list[4]):
            self.df.loc[i, 'Geo Loc'] = geoLoc_list[3]
        
        # adding Geo Loc tags for the fourth geoLoc (not include US total
        for i in range(index_list[4]+1, index_list[5]):
            self.df.loc[i, 'Geo Loc'] = geoLoc_list[4]
        
        # adding Geo Loc tags for the fifth geoLoc (not include US total
        for i in range(index_list[5]+1, index_list[6]):
            self.df.loc[i, 'Geo Loc'] = geoLoc_list[5]
        
        # adding Geo Loc tags for the sixth geoLoc (not include US total
        for i in range(index_list[6]+1, index_list[7]):
            self.df.loc[i, 'Geo Loc'] = geoLoc_list[6]
        
        # adding Geo Loc tags for the seventh geoLoc (not include US total
        for i in range(index_list[7]+1, index_list[8]):
            self.df.loc[i, 'Geo Loc'] = geoLoc_list[7]
        
        # adding Geo Loc tags for the eighth geoLoc (not include US total
        for i in range(index_list[8]+1, len(self.df[columnNameofStates])):
            self.df.loc[i, 'Geo Loc'] = geoLoc_list[8]
        
        # return DataFrame to ensure 
        return self.df

            
            
    def restructureDataFrame(self, columnNameofStates = 'Cleaned Area'):
# =============================================================================
#         Restructuring the DataFrame so that each state from each year is a
#         separate data point
#           -columnNameofStates: optional; only needed if user changed the
#                                column name to something else
# =============================================================================
        states = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia",
          "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", 
          "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", 
          "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", 
          "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", 
          "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
        
        # empty DataFrame to hold the new columns
        GDPdf = pd.DataFrame()
        # count variable to increase the index by one after each row is added
        count = 0
        
        # for loop to iterate through the years specified by the instance
        for year in range(self.yearStart, self.yearEnd + 1):
            # for each state in that year, add in the following columns
            for state in states:
                GDPdf.loc[count, 'year'] = str(year)
                GDPdf.loc[count, 'state'] = state
                GDPdf.loc[count, 'current dollars'] = self.dollars
                GDPdf.loc[count, 'GDP'] = float(re.sub('[,*]','',
                                                 self.df.loc[self.df[columnNameofStates] == state, str(year)].item()))
                GDPdf.loc[count, 'GDP_area'] = self.df.loc[self.df[columnNameofStates] == state, 'Geo Loc'].item()
                count += 1
        
        # reassign new DataFrame to the instance
        self.df = GDPdf
        
        # return new DataFrame to verify columns and rows were added as intended
        return self.df

    
    def splitColumns(self, columnIndex, leftColumnName, rightColumnName):
# =============================================================================
#     Method to split columns that were put together when the tables was read
#       -columnIndex: the column where the data needs to be split
#       -leftColumnName: column name for the data on the left
#       -rightColumnName: column name for the data on the right
# =============================================================================
        
        # lists to hold the values from each row
        list1 = []
        list2 = []
        
        # loop through the index
        for i in self.df.index:
            splitList = self.df.iloc[i, columnIndex].split(" ")
            list1.append(splitList[0])
            list2.append(splitList[1])
        
        for i in self.df.index:
            self.df.loc[i, leftColumnName] = list1[i]
            self.df.loc[i, rightColumnName] = list2[i]
        
        return self.df


class QuarterlyGDP(YearlyGDP):
    
    def __init__(self, file, pageNum, yearStart, yearEnd, dollars,
                           df = pd.DataFrame()):
        YearlyGDP.__init__(self, file, pageNum, yearStart, yearEnd, dollars,
                           df = pd.DataFrame())
    
    

                
            