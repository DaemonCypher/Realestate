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

A more likely option is to only keep track of a city or state instead of the entire U.S. if used for personal reasons.

The code will be develop with SQlite3 as the backend database, Python3 for data collection, organization, and API for the frontend to communicate to. Node.js and D3.js will be used for grabing the data in the back and displaying charts in the frontend. 

# Prequiste
* Anaconda
* Vscode
* Python3
* Node.js
* some kind of Zip file unpacker
  
# Install libraries
```
npm install express sqlite3 body-parser d3
```
```
pip install requests aiohttp geopandas alive-progress
```

# To run the code
Download the region of realestate to look at from [openAddress.io](https://batch.openaddresses.io/data#map=0/0/0 "@embed"); this will reguire you to have an account with openAddress.io. 
Would recommend only downloading the files for the region you want to look at as the files downloaded are quite large and with file processing and creation the code size will be quite large (rough estimate with all states/regions ~50gb).

Unpack the downloaded files and drop them in \Realestae\Download folder. Run the following command in the root directory. This will start collecting data from state you want to look at, 
depending on the state this will take a while. A 100,000 address takes about 42 minutes this is with 32gb ram. The code can be ran in chunks so if you are not able to run the code for several hours you can run the code in increments of 100,000(more or less)
untill you have grab all the address from the state.

```
python3 setup.py
```

Will start the webpage with all the data collected and display the chart.
```
npm run start
```

# To be implemented
* Candle Stick chart
* OpenAddresses webscraper(might be easier to have the user download the data instead)
* Webpage
* Hosting the code
* Implement d3.js for front end view
* U.S. county choropleth heat map
* argparse for setup.py
