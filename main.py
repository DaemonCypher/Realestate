from getAdresses import *
import os 
#import map
import helper
from statenames import *
# when downloading addresses from openAddresses look for the statewide addresses file

def main():

    
    print("What region of the U.S. realestate would you like to at")
    region = input("NE(North East), S(South), MW(Mid West),W(West)\n: ")
    region = region.lower()
    region= region.replace(" ","")
    print(abbreviations(region))
    # TODO: here download files from openAddresses based on user input
    state = input("What state would you like to look at\n: ")
    print()
    # TODO: here clean up the downloaded files to only the state file the user wants
    print("Do you want addresses from a city")
    city_toggle = input("(Y)es/(N)o\n: ")
    city_toggle.lower()
    print()
    if city_toggle =='y':
        # TODO: list the city names from a state(i.e. statname subfolder)
        city = input("What city would you like to look at\n:")
    else:
        print("Showing {} realestate information".format(state.upper()))
    
    # 
        
 
    
    
    
main()

    
    
    
    
    