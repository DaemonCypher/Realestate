# Real Estate Heat Map /Historic Price Trend Indicator.

This is an individual project for nation wide heat map of the U.S. by county, and can be viewed downed to the city for more accurate representation and details on a city level. 


Currently a working progress. Main issue is the amount of data to be process (CT alone has 1015948 known addresses)
,and as of right now after modifying Redfin unofficial api (https://pypi.org/project/redfin/) and running the code in parallel give us about 40-60 address computed per second. 
This is after removing several duplicate addresses and addresses that are likely to be apartments.
Without a backing of an organization to use Zillow API for faster request time or more request it is feasibly impossible to run the code alone on a personal computer for a nation wide scale.

A more likely option is to only keep track of a city or state instead of the entire U.S. if used for personal reasons.

Tech Stack: Python3, SQLite3, Node.js, Express.js 

# Prequiste
* Anaconda
* Vscode
* Python3
* Node.js
* some kind of Zip file unpacker
* Npm
* Pip
  
# Install libraries
```
npm install express sqlite3 body-parser child_process gridstack  tablefilter
```
```
pip install requests aiohttp geopandas tqdm pandas numpy tensorflow scikit-learn
```

# Intial Setup
Download the region of realestate to look at from [openAddress.io](https://batch.openaddresses.io/data#map=0/0/0 "@embed"); this will reguire you to have an account with openAddress.io. 
Would recommend only downloading the files for the region you want to look at as the files downloaded are quite large and with file processing and creation the code size will be quite large (rough estimate with all states/regions ~150gb).

Unpack the downloaded files and drop them in \Realestae\downloads folder. Run the following command in the root directory. This will start collecting data from state you want to look at, 
depending on the state this will take a while. A 100,000 address takes about 42 minutes this is with 32gb ram. The code can be ran in chunks so if you are not able to run the code for several hours you can run the code in increments of 100,000(more or less) untill you have grab all the address from the state. If ran with 100,000 the first time, then to grab the next 100,000 you will need to modify the -i flag to be "-i 200000".

```
python3 setup.py -i 1000 -n ct -f
```
-i flag for how many address to be proccess(Required). The value after is the number of addresses to be processed.


-n flag for the state to be proccess(Required). The value after is the state name abbreviation of addresses to be processed.


-f flag to convert the file and remove unnecessary addresses. Only need to use the flag once for the first run of a new state(Optional).


# Dispaly Web App
Will start the webpage with all the data collected and display the chart.
```
npm run start
```
![](https://github.com/DaemonCypher/Realestate/blob/main/demo.gif)

# Price Prediction
It is recommended that you have collected all the addresses from setup.py before executing the code below as the model will perform better with more data.
```
python3 ml_setup.py [city_name]
```
Replace [city_name] with a name of a city from the data you have collected.
# To be implemented
* Add assets and restructure webpage from/with Figma
* Hosting the code at Vercel with a demo database to grab property data
* Containarize code
* Add feature for process_geojson_data() to write in batches while collecting data instead of after
* Connect front end to back end machine learning price prediction
* Update demo
