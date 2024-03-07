import json
import pandas as pd
from pandas import json_normalize

class Restaurant():
    def __init__(self, restaurant_data, country_code):
        self.country_code = pd.read_excel(country_code)
        self.restaurant_data = restaurant_data
        self.restaurant_data = self.load_data()

    def load_data(self):
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
        # extract keys and create individual columns
        loc_columns = list(self.restaurant_data.loc[0, 'location'].keys())
        for key in loc_columns:
            self.restaurant_data[key] = self.restaurant_data['location'].apply(lambda x: x.get(key, 'NA'))

    def extract_ratings(self):
        # extract keys and create individual columns
        rating_columns = list(self.restaurant_data.loc[0, 'user_rating'].keys())
        for key in rating_columns:
            # print(key)
            self.restaurant_data[key] = self.restaurant_data['user_rating'].apply(lambda x: x.get(key, 'NA'))

    def get_country(self):
        left_key_col = 'country_id'
        right_key_col = 'Country Code'
        self.restaurant_data = pd.merge(self.restaurant_data, self.country_code, left_on = left_key_col, right_on = right_key_col, how='left')

    def get_restaurants(self):
        fields = ['id', 'name', 'Country', 'city', 'votes', 'aggregate_rating', 'cuisines']
        data_type = {'id': 'int32', 'name': 'str', 'Country': 'str', 'city': 'str', 'votes': 'int32', 'aggregate_rating': 'float32', 'cuisines': 'str'}
        col_names = {'id': 'Restaurant Id', 'name': 'Restaurant Name', 'Country': 'Country', 'city': 'City', 'votes': 'User Rating Votes', 'aggregate_rating': 'User Aggregate Rating', 'cuisines': 'Cuisines'}

        self.restaurants = self.restaurant_data[fields].astype(data_type)
        self.restaurants.rename(columns=col_names, inplace=True)

        self.restaurants.to_csv('restaurants.csv', index=False)




                                        


    

if __name__ == "__main__":
    restaurant_data = 'Data/restaurant_data.json'
    country_code = 'Data/Country-Code.xlsx'
    restaurant = Restaurant(restaurant_data, country_code)
    restaurant.extract_location()
    restaurant.get_country()
    restaurant.extract_ratings()
    restaurant.fill_empty_values()
    restaurant.get_restaurants()
    # restaurant.restaurant_data.to_csv('restaurant_data2.csv', index=False)


