# Realestate
Real Estate Heat Map /Historic Price Trend Indicator.

This is an individual project for nation wide heat map of the U.S. by county, and can be viewed downed to the city for more accurate representation.
It will also incorprate a historic price trend in a form of a candle stick chart (without the low and high, as the data will only be updated 
once a month with the begining and end of the 30 day period) on the scale of what the user is viewing at the time. This can be a nation wide
candle stick chart or a small city candle stick chart. Each time new data is gathered or update the average price of that region will be updated
with the corresponding new data. 


Currently a working progress. Main issue is the amount of data to be process(CT alone has 1015948 known addresses)
,and as of right now after modifying Redfin unofficial api (https://pypi.org/project/redfin/) and running the code in parallel give us about 40 address computed per second. 
This is after removing several duplicate addresses and addresses that are likely to be apartments.
Without a backing of an organization to use Zillow API for faster request time or more request it is feasibly impossible to run the code alone on a personal computer for a nation wide scale.
Will still be working on creating components of the project, but the complete implementation of the project will not be done for the reasons mentioned before.

A more likely option is to only keep track of a city instead of the entire U.S. if used for personal reasons.

# To be implemented
* Candle Stick chart
* OpenAddresses webscraper
* Webpage
* Hosting the code
* Implement d3.js for front end view
* U.S. county choropleth heat map 
