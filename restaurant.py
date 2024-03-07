import json
import pandas as pd
from pandas import json_normalize
import numpy as np

class Restaurant():
    '''
    A class for loading restaurant data and country code information.

    This class loads restaurant data and country code information from the given
    files and provides methods for accessing and manipulating this data.

    The required tasks and files will be generated.
    '''
    def __init__(self, restaurant_data, country_code):
        '''
        Initialize the Restaurant object.

        Args:
            restaurant_data (json file): The file path containing restaurant data.
            country_code (excel file): The file path containing country code information.
        '''
        self.country_code = pd.read_excel(country_code)
        self.restaurant_data = restaurant_data
        self.restaurant_data = self.load_data()

    def load_data(self):
        '''
        This method reads the specified JSON file containing restaurant data,
        extracts relevant information, and stores it in a pandas DataFrame.
        '''
        # load restaurant_data.json 
        with open(self.restaurant_data) as f:
            data = json.load(f)

        # extract data from restaurants list
        restaurant_data = []
        for item in data:
            restaurants = item.get('restaurants', [])
            for restaurant in restaurants:
                restaurant_data.append(restaurant.get('restaurant', {}))

        # store extracted restaurant data in a dataframe
        df = pd.DataFrame(restaurant_data)
        return df
    
    def fill_empty_values(self):
        self.restaurant_data = self.restaurant_data.replace('', 'NA')
        self.restaurant_data = self.restaurant_data.fillna('NA')

    def extract_location(self):
        '''
        Extract location information from the 'location' column in the DataFrame.

        This method extracts location information from the 'location' column, which contains
        a dictionary with various location details such as address, locality, city, etc.
        It creates individual columns for each location detail extracted.
        '''
        # extract keys and create individual columns
        loc_columns = list(self.restaurant_data.loc[0, 'location'].keys())
        for key in loc_columns:
            self.restaurant_data[key] = self.restaurant_data['location'].apply(lambda x: x.get(key, 'NA'))

    def extract_ratings(self):
        '''
            Extract ratings information from the 'user_rating' column in the DataFrame.

            This method extracts rating information from the 'user_rating' column, which contains
            a dictionary with various rating details such as aggregate_rating, rating_text, votes, etc.
            It creates individual columns for each rating detail extracted.
        '''
        # extract keys and create individual columns
        rating_columns = list(self.restaurant_data.loc[0, 'user_rating'].keys())
        for key in rating_columns:
            # print(key)
            self.restaurant_data[key] = self.restaurant_data['user_rating'].apply(lambda x: x.get(key, 'NA'))

    def get_country(self):
        '''
        Merge restaurant dataframe with country code spreadsheet to get country information.
        '''
        left_key_col = 'country_id'
        right_key_col = 'Country Code'
        self.restaurant_data = pd.merge(self.restaurant_data, self.country_code, left_on = left_key_col, right_on = right_key_col, how='left')

    def get_restaurants(self):
        '''
        Generates a CSV file containing the required restaurant information (Task 1).
        '''
        fields = ['id', 'name', 'Country', 'city', 'votes', 'aggregate_rating', 'cuisines']     # required columns
        data_type = {'id': 'int32', 'name': 'str', 'Country': 'str', 'city': 'str', 'votes': 'int32', 'aggregate_rating': 'float32', 'cuisines': 'str'}
        col_names = {'id': 'Restaurant Id', 'name': 'Restaurant Name', 'Country': 'Country', 'city': 'City',
                     'votes': 'User Rating Votes', 'aggregate_rating': 'User Aggregate Rating', 'cuisines': 'Cuisines'}

        self.restaurants = self.restaurant_data[fields].astype(data_type)
        self.restaurants.rename(columns=col_names, inplace=True)

        self.restaurants.to_csv('restaurants.csv', index=False)

    def get_events(self):
        '''
        Generates a CSV file for event information during the period April 2019 (Task 2)
        '''
        # subset data containing required fields
        event_data = self.restaurant_data[['id', 'name', 'zomato_events']] 
        # drop rows with no events
        event_data = event_data[event_data['zomato_events']!='NA']

        # get individual events for each restaurant (currently stored as a list of events)
        event_data = event_data.explode('zomato_events')
        # remove event key
        event_data['zomato_events'] = event_data['zomato_events'].apply(lambda x: list(x.values())[0])

        # extract keys (event information) and create individual columns
        event_columns = list(event_data.loc[0, 'zomato_events'].keys())
        for key in event_columns:
            event_data[key] = event_data['zomato_events'].apply(lambda x: x.get(key, 'NA'))

        # convert date format
        event_data['start_date'] = pd.to_datetime(event_data['start_date'], format='%Y-%m-%d')
        event_data['end_date'] = pd.to_datetime(event_data['end_date'], format='%Y-%m-%d')

        # extract events in April 2019
        april_events = event_data[event_data['start_date'].dt.strftime('%Y-%m') == '2019-04']

        # extract photo url
        april_events['photo_url'] = april_events['photos'].apply(lambda x: x[0]['photo']['url'] if x else 'NA')

        # required fields
        april_events = april_events[['event_id', 'id', 'name', 'photo_url', 'title', 'start_date', 'end_date']]

        # rename columns
        col_names = {'event_id': 'Event Id', 'id': 'Restaurant Id', 'name': 'Restaurant Name', 'photo_url': 'Photo URL',
                     'title': 'Event Title', 'start_date': 'Event Start Date', 'end_date': 'Event End Date'}
        april_events.rename(columns=col_names, inplace=True)

        self.april_events = april_events
        self.april_events.to_csv('retaurant_events.csv', index = False)

    def rating_threshold(self):
        '''
            Generates a CSV file for ratings threshold for the follwong values:
            Excellent, Very Good, Good, Average, Poor
        '''
        ratings = self.restaurant_data[['aggregate_rating', 'rating_text']]
        text_ratings = ['Excellent', 'Very Good', 'Good', 'Average', 'Poor']
        self.ratings = ratings[ratings['rating_text'].isin(text_ratings)]
        threshold = self.ratings.groupby('rating_text')['aggregate_rating'].agg(['min', 'max'])
        threshold = threshold.apply(lambda x: x.reindex(text_ratings))

        # change max and min values for ratings
        threshold.loc['Excellent', 'max'] = 5.0
        threshold.loc['Poor', 'min'] = 0.0

        # ensure ratings are in a continous range 
        threshold.loc['Poor', 'max'] = str(float(threshold.loc['Average', 'min']) - 0.1)
        self.threshold = threshold

        self.threshold.to_csv('threshold.csv')

    def run_all_tasks(self):
        self.extract_location()
        self.extract_ratings()
        self.get_country()
        self.fill_empty_values()
        self.get_events()
        self.get_restaurants()
        self.rating_threshold()


if __name__ == "__main__":
    restaurant_data = 'Data/restaurant_data.json'
    country_code = 'Data/Country-Code.xlsx'
    restaurant = Restaurant(restaurant_data, country_code)
    restaurant.run_all_tasks()

    # print(restaurant.threshold)     # uncomment this to print ratings threshold



