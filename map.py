import folium
from geoCords import *
from getDetails import *
from alive_progress import alive_bar
import folium.plugins as plugins
def create_us_map_combined():
    # Base map
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4, tiles='OpenStreetMap')  # Coordinates for the center of the US

    # Add state and county boundaries with different styles
    # Styling function for state boundaries
    def state_style(feature):
        return {
            'color': '#4CAF50',  # Green for state boundaries
            'weight': 2
        }

    # Styling function for county boundaries
    def county_style(feature):
        return {
            'color': '#FFC107',  # Orange for county boundaries
            'weight': 1
        }

    # Add state boundary to the map using GeoJSON data
    state_boundary_url = 'https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_5m.json'
    folium.GeoJson(
        state_boundary_url,
        name='State Boundaries',
        style_function=state_style,
        overlay=True
    ).add_to(m)

    # Add county boundary to the map using GeoJSON data
    county_boundary_url = 'https://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_050_00_20m.json'
    folium.GeoJson(
        county_boundary_url,
        name='County Boundaries',
        style_function=county_style,
        overlay=True
    ).add_to(m)

    
    geojson_file_path = '' 
    geojson_data = read_geojson_features(geojson_file_path)
    heat_data = []  # Stores the coordinates and intensity for the heatmap
    # Add the addresses from GeoJSON data as markers

    '''for feature in geojson_data:
        coords = feature["geometry"]["coordinates"]
        props = feature["properties"]
        address = f"{props['number']} {props['street']}, {props['city']}, {props['region']} {props['postcode']}"
        
        folium.Marker(
            location=[coords[1], coords[0]],
            popup=address,
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)        
        '''    
    count = 0
    # can add len of the geojson file
    with alive_bar(title='Processing addresses and plotting points on map',spinner ='dots_wave') as bar:
        while count < 100:
            feature = geojson_data[count]
            coords = feature["geometry"]["coordinates"]
            props = feature["properties"]
            address = f"{props['number']} {props['street']}, {props['city']}, {props['region']} {props['postcode']}"
            data = getDetails(address)
            
            if data =="":
                # want to ingore land, builidings, and other properties that are not homes
                pass
            else:
                if data['payload']['isActivish'] ==False:
                    listing_price = "None"
                else:
                    listing_price = data['payload']['listingPrice']
                    
                num_beds = data['payload']['numBeds']
                num_baths = data['payload']['numBaths']
                sq_ft = data['payload']['sqFt']['value']
                price_amount = data['payload']['priceInfo']['amount']
                predicted_value = data['payload']['predictedValue']
                popup_content = """
                <p>Address: {}</p>
                <p>Number of Beds: {}</p>
                <p>Number of Baths: {}</p>
                <p>Square Feet: {}</p>
                <p>Listing Price: {}</p>
                <p>Price Amount: {}</p>
                <p>Predicted Value: {}</p>
                """.format(address,num_beds,num_baths,sq_ft,listing_price,price_amount,predicted_value)


                popup = folium.Popup(popup_content, max_width=300)
                folium.Marker(
                    location=[coords[1], coords[0]],
                    popup=popup,
                    icon=folium.Icon(icon="home"),
                ).add_to(m) 
            
            count += 1
            bar()
        

    # Add LayerControl to toggle layers
    folium.LayerControl().add_to(m)

    # Save map to HTML file
    m.save('us_map_combined.html')

create_us_map_combined()


