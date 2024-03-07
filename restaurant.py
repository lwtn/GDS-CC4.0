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
    


    

if __name__ == "__main__":
    restaurant_data = 'Data/restaurant_data.json'
    country_code = 'Data/Country-Code.xlsx'
    restaurant = Restaurant(restaurant_data, country_code)
    # restaurant.restaurant_data.to_csv('restaurant_data.csv', index=False)