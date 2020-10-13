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

    def __init__(self, file, pageNum, yearStart, yearEnd, df = pd.DataFrame()):
        self.file = file
        self.pageNum = pageNum
        self.yearStart = yearStart
        self.yearEnd = yearEnd
        self.df = df
    
    
    def initializeDataFrame(self):
        # read the PDF and return the DataFrame for viewing
        list_df = tabula.read_pdf(self.file, pages = self.pageNum, stream = True)
        self.df = list_df[0]
        
        # read the column names from the DataFrame
        self.df.iloc[0].apply(str)
        
        for i in range(len(self.df.columns)):
            try:
                if self.df.iloc[0,i].isnumeric():
                    pass
                else:
                    self.df.iloc[0, i] = re.sub("[\/a-zA-Z*]",'', self.df.iloc[0, i])
            except AttributeError:
                if self.df.iloc[0,i].is_integer():
                    pass
                else:
                    "Attempting the change column names..."
                    
        self.df.iloc[0,0] = 'Area'
        self.df.iloc[0,len(self.df.columns)-1] = 'Percentage of U.S. total'
        
        name = self.df.loc[0,]
        self.df = self.df.rename(columns = name).drop(self.df.index[0]).reset_index(drop = True)
        
        # return the DataFrame for viewing
        return self.df
        
    
    def cleanStates(self, columnName):
        # make sure the column specified is string type
        if self.df[columnName].dtype == 'str':
            pass
        else:
            self.df[columnName] = self.df[columnName].astype('str')
        
        # clean the white space and periods from the area column
        # create a list to hold the cleaned area names
        clean_areas = []
        for i in self.df[columnName].index:
            try:
                if math.isnan(self.df.loc[i, columnName]):
                    pass
                else:
                    area = self.df.loc[i, columnName]
                    #print(area)
                    clean_areas.append(' '.join(re.sub("[\s\.*]"," ", area).split()))
            except TypeError:
                area = self.df.loc[i, columnName]
                #print(area)
                clean_areas.append(' '.join(re.sub("[\s\.*]"," ", area).split()))
            
        # Loop through the list to add the cleaned areas back into the DataFrame using loc() method
        for i in self.df[columnName].index:
            try:
                if math.isnan(self.df.loc[i, columnName]):
                    pass
                else:
                    #print(i-1)
                    self.df.loc[i , f'Cleaned {columnName}'] = clean_areas[i]
            except TypeError:
                self.df.loc[i , f'Cleaned {columnName}'] = clean_areas[i]
        
        return self.df
    
    def addGeoLocColumn(self, columnNameofStates):
        summary = ['United States', 'New England', 'Mideast', 'Great Lakes',
           'Plains', 'Southeast', 'Southwest', 'Rocky Mountain', 'Far West']
        geoLoc_list = []
        index_list = []
        
        for i in self.df[columnNameofStates].index:
            try:
                if math.isnan(self.df.loc[i, columnNameofStates]):
                    pass
                else:
                    if self.df.loc[i, columnNameofStates] in summary:
                        geoLoc_list.append(self.df.loc[i, columnNameofStates])
                        index_list.append(i)
            except TypeError:
                if self.df.loc[i, columnNameofStates] in summary:
                        geoLoc_list.append(self.df.loc[i, columnNameofStates])
                        index_list.append(i)
                        
                        
        
        for i in range(index_list[1]+1, index_list[2]):
            self.df.loc[i, 'Geo Loc'] = 'New England'
        for i in range(index_list[2]+1, index_list[3]):
            self.df.loc[i, 'Geo Loc'] = 'Mideast'
        for i in range(index_list[3]+1, index_list[4]):
            self.df.loc[i, 'Geo Loc'] = 'Great Lakes'
        for i in range(index_list[4]+1, index_list[5]):
            self.df.loc[i, 'Geo Loc'] = 'Plains'
        for i in range(index_list[5]+1, index_list[6]):
            self.df.loc[i, 'Geo Loc'] = 'Southeast'
        for i in range(index_list[6]+1, index_list[7]):
            self.df.loc[i, 'Geo Loc'] = 'Southwest'
        for i in range(index_list[7]+1, index_list[8]):
            self.df.loc[i, 'Geo Loc'] = 'Rocky Mountain'
        for i in range(index_list[8]+1, len(self.df[columnNameofStates])):
            self.df.loc[i, 'Geo Loc'] = 'Far West'
        
        return self.df

            
            
    def restructureDataFrame(self, columnNameofStates):
        states = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia",
          "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", 
          "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", 
          "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", 
          "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", 
          "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
        
        GDPdf = pd.DataFrame()
        count = 0
        
        for year in range(self.yearStart, self.yearEnd + 1):
            for state in states:
                GDPdf.loc[count, 'year'] = str(year)
                GDPdf.loc[count, 'state'] = state
                GDPdf.loc[count, 'GDP'] = self.df.loc[self.df[columnNameofStates] == state, str(year)].item()
                GDPdf.loc[count, 'GDP_area'] = self.df.loc[self.df[columnNameofStates] == state, 'Geo Loc'].item()
                count += 1
        
        self.df = GDPdf
        return self.df

    
    def splitColumns(self, columnIndex, leftColumnName, rightColumnName):
        list1 = []
        list2 = []
        
        for i in self.df.index:
            splitList = self.df.iloc[i, columnIndex].split(" ")
            list1.append(splitList[0])
            list2.append(splitList[1])
        
        for i in self.df.index:
            self.df.loc[i, leftColumnName] = list1[i]
            self.df.loc[i, rightColumnName] = list2[i]
        
        return self.df


class QuarterlyGDP(YearlyGDP):
    
    def __init__(self):
        pass
