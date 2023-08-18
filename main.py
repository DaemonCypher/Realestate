from getAdresses import *
import os 
import map
import cleaner
import downloader
from statenames import *
# when downloading addresses from openAddresses look for the statewide addresses file

def main():
    state = ""
    city = ""
    print("What region of the U.S. realestate would you like to at")
    region = input("NE(North East), S(South), MW(Mid West),W(West)\n:")
    region = region.lower()
    region= region.replace(" ","")
    print(abbreviations(region))
    city_toggle = input("Do you want addresses from a city ")
    print()
    
    
    
main()

    
    
    
    
    
