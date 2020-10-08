# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 17:12:50 2020
Web Scrape Mean Gross Richmond, VA Rental Prices for 2006 - 2013
and Mean Gross Rental Prices in Virginia Beach for 2006 - 2013
"""

# Import Libraries I will need
import requests # import requests library
from bs4 import BeautifulSoup # import BeautifulSoup library
import csv 


def writeRentalPricesToCSV(rental_price_list, filename):
    """ writeRentalPricesToCSV(rental_price_list, filename): write contents of list to csv file (filename)"""
   
    try:
        with open(filename, 'w+', newline='') as f: 
            w = csv.DictWriter(f,['yr','period','frequency','location_name','median_rent_price','mean_rent_price']) 
            for item in rental_price_list: 
                w.writerow(item)
    except IOError as err:
        print("An IO Error has been raised: " + str(err))
    except PermissionError as err:
        print("The file may be open or I don't have rights to write to it: " + str(err))
    except Exception as err:
        print("A General Exception has been raised: " + str(err))

def retrieveLoopableSoupFind(url, parentTag, searchAttrs):
    """retrieveLoopableSoupFind(url, parentTag, searchAttrs): return a soup tag by beautifulSoup filter attribute"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup.find(parentTag, attrs = searchAttrs) 
    except Exception as err:
        print("A General Exception has been raised: " + str(err))
        
def retrieveLoopableSoupFindAll(url, parentTag, searchAttrs):
    """retrieveLoopableSoupAll(url, parentTag, searchAttrs): return an iterable collection of soup tags by beautifulSoup filter attribute"""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup.findAll(parentTag, attrs = searchAttrs) 
    except Exception as err:
        print("A General Exception has been raised: " + str(err))   

def retrieveCityRents(url, rentTableId, cityName, filename):
    """"Retrieve the table of real gross rental history for the city"""
    try:
        rentTable = retrieveLoopableSoupFind(url, 'table', {'id': rentTableId})
        
        rents = []  # a list to store quotes      
        
        #create the header row
        rents.append({'yr':'yr','period':'period','frequency':'frequency','location_name':'location_name','median_rent_price':'median_rent_price','mean_rent_price':'mean_rent_price'})
        
        # loop through table tr / td
        for tr in rentTable.findAll('tr'):
            cellCounter = 0
            rentyear = {}
            
            for td in tr.findAll('td'):
                if (cellCounter == 0):
                    rentyear['yr'] = td.contents[0]
                    rentyear['period'] = "1"
                    rentyear['frequency'] = "year"
                    rentyear['location_name'] = cityName
                elif (cellCounter == 3):
                    rentyear['median_rent_price'] = td.contents[0]
                elif (cellCounter == 4):
                    rentyear['mean_rent_price'] = td.contents[0]
                cellCounter += 1
            # append the year to the list of all the years        
            rents.append(rentyear)
        
        # write the list to the csv file
        writeRentalPricesToCSV(rents, filename)
    except Exception as err:
            print("A General Exception during Richmond retrieval has been raised: " + str(err))
  
        
retrieveCityRents('https://www.deptofnumbers.com/rent/virginia/richmond/','table_586508','Richmond, VA','RichmondRent.csv' )

retrieveCityRents('https://www.deptofnumbers.com/rent/virginia/virginia-beach-city/','table_744304','Virginia Beach, VA','VABeachRent.csv' )