# Realestate
Real Estate Heat Map /Historic Price Trend Indicator.

This is an individual project for nation wide heat map of the U.S., and can be viewed downed to the city for more accurate representation.
It will also incorprate a historic price trend in a form of a candle stick chart (without the low and high, as the data will only be updated 
once a month with the begining and end of the 30 day period) on the scale of what the user is viewing at the time. This can be a nation wide
candle stick chart or a small city candle stick chart. Each time new data is gathered or update the average price of that region will be updated
with the corresponding new data. If the user views the map on a city level lattidute and longitude positions of buildings can be viewed, and if clicked on
it will show number of beds, number of baths, square feet, listing price, is serviced, is active, price amount, predicted value of the property, and a link
to redfin of the property for further information such as images and etc...

Currently a working progress. Main issue is the amount of data to be process(CT alone has 1015948 known addresses)
,and as of right now Redfin unofficial api (https://pypi.org/project/redfin/) takes about ~5 seconds per request (i.e. address).
Without a backing of an organization to use Zillow API for faster request time or a server run in parrallel to split the work of
the data it is feasibly impossible to run the code alone on a personal computer. Will still be working on creating components of the project
, but the complete implementation of the project will not be done for the reasons mentioned before.

A more likely option is to only keep track of a city instead of the entire U.S. if used for personal reasons.

# To be implemented
* Heat Map
* Candle Stick chart
* Back end storage
* OpenAddresses webscraper
* Webpage
* Hosting the code


