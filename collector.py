import requests
import json
import aiohttp
# The Class Redfin is taken from https://github.com/reteps/redfin 
# converted it to async for faster run time.
class Redfin:
    def __init__(self):
        self.base = 'https://redfin.com/stingray/'
        self.user_agent_header = {
            'user-agent': 'redfin'
        }

    async def meta_request(self, url, kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base + url, params=kwargs, headers=self.user_agent_header
            ) as response:
                if response.status != 200:
                    raise aiohttp.ClientError(f"Request failed with status {response.status}")
                response_text = await response.text()
                return json.loads(response_text[4:])

    async def meta_property(self, url, kwargs, page=False):
        if page:
            kwargs['pageType'] = 3
        return await self.meta_request('api/home/details/' + url, {
            'accessLevel': 1,
            **kwargs
        })

    # Url Requests

    async def initial_info(self, url, **kwargs):
        return await self.meta_request('api/home/details/initialInfo', {'path': url, **kwargs})

    async def page_tags(self, url, **kwargs):
        return await self.meta_request('api/home/details/v1/pagetagsinfo', {'path': url, **kwargs})

    async def primary_region(self, url, **kwargs):
        return await self.meta_request('api/home/details/primaryRegionInfo', {'path': url, **kwargs})

    # Search
    async def search(self, query, **kwargs):
        return await self.meta_request('do/location-autocomplete', {'location': query, 'v': 2, **kwargs})

    # Property ID Requests
    async def below_the_fold(self, property_id, **kwargs):
        return await self.meta_property('belowTheFold', {'propertyId': property_id, **kwargs}, page=True)

    async def hood_photos(self, property_id, **kwargs):
        return await self.meta_request('api/home/details/hood-photos', {'propertyId': property_id, **kwargs})

    async def more_resources(self, property_id, **kwargs):
        return await self.meta_request('api/home/details/moreResourcesInfo', {'propertyId': property_id, **kwargs})

    async def page_header(self, property_id, **kwargs):
        return await self.meta_request('api/home/details/homeDetailsPageHeaderInfo', {'propertyId': property_id, **kwargs})

    async def property_comments(self, property_id, **kwargs):
        return await self.meta_request('api/v1/home/details/propertyCommentsInfo', {'propertyId': property_id, **kwargs})

    async def building_details_page(self, property_id, **kwargs):
        return await self.meta_request('api/building/details-page/v1', {'propertyId': property_id, **kwargs})

    async def owner_estimate(self, property_id, **kwargs):
        return await self.meta_request('api/home/details/owner-estimate', {'propertyId': property_id, **kwargs})

    async def claimed_home_seller_data(self, property_id, **kwargs):
        return await self.meta_request('api/home/details/claimedHomeSellerData', {'propertyId': property_id, **kwargs})

    async def cost_of_home_ownership(self, property_id, **kwargs):
        return await self.meta_request('do/api/costOfHomeOwnershipDetails', {'propertyId': property_id, **kwargs})

    # Listing ID Requests
    async def floor_plans(self, listing_id, **kwargs):
        return await self.meta_request('api/home/details/listing/floorplans', {'listingId': listing_id, **kwargs})

    async def tour_list_date_picker(self, listing_id, **kwargs):
        return await self.meta_request('do/tourlist/getDatePickerData', {'listingId': listing_id, **kwargs})

    # Table ID Requests

    async def shared_region(self, table_id, **kwargs):
        return await self.meta_request('api/region/shared-region-info', {'tableId': table_id, 'regionTypeId': 2, 'mapPageTypeId': 1, **kwargs})

    # Property Requests

    async def similar_listings(self, property_id, listing_id, **kwargs):
        return await self.meta_property('similars/listings', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    async def similar_sold(self, property_id, listing_id, **kwargs):
        return await self.meta_property('similars/solds', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    async def nearby_homes(self, property_id, listing_id, **kwargs):
        return await self.meta_property('nearbyhomes', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    async def above_the_fold(self, property_id, listing_id, **kwargs):
        return await self.meta_property('aboveTheFold', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    async def property_parcel(self, property_id, listing_id, **kwargs):
        return await self.meta_property('propertyParcelInfo', {'propertyId': property_id, 'listingId': listing_id, **kwargs}, page=True)

    async def activity(self, property_id, listing_id, **kwargs):
        return await self.meta_property('activityInfo', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    async def customer_conversion_info_off_market(self, property_id, listing_id, **kwargs):
        return await self.meta_property('customerConversionInfo/offMarket', {'propertyId': property_id, 'listingId': listing_id, **kwargs}, page=True)

    async def rental_estimate(self, property_id, listing_id, **kwargs):
        return await self.meta_property('rental-estimate', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    async def avm_historical(self, property_id, listing_id, **kwargs):
        return await  self.meta_property('avmHistoricalData', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    async def info_panel(self, property_id, listing_id, **kwargs):
        return await self.meta_property('mainHouseInfoPanelInfo', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    async def descriptive_paragraph(self, property_id, listing_id, **kwargs):
        return await self.meta_property('descriptiveParagraph', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    async def avm_details(self, property_id, listing_id, **kwargs):
        return await self.meta_property('avm', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    async def tour_insights(self, property_id, listing_id, **kwargs):
        return await self.meta_property('tourInsights', {'propertyId': property_id, 'listingId': listing_id, **kwargs}, page=True)

    async def stats(self, property_id, listing_id, region_id, **kwargs):
        return await self.meta_property('stats', {'regionId': region_id, 'propertyId': property_id, 'listingId': listing_id, 'regionTypeId': 2, **kwargs})
    
    
    # Added additional function here to better suit the project needs. This function uses the propertyID and gathers estimated historical price
    # history from redfin.
    async def price_history(self, property_id, listing_id=None, **kwargs):
        params = {'propertyId': property_id}
        if listing_id:
            params['listingId'] = listing_id
        params.update(kwargs)
        return await self.meta_property('avmHistoricalData', params)
    
    
