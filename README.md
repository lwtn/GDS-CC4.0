# GDS-CC4.0
## About
This project looks into restaurant data from Zomato and completes the following tasks:
### Task 1
Extract the following fields and store the data as restaurants.csv.
- Restaurant Id
- Restaurant Name
- Country
- City
- User Rating Votes
- User Aggregate Rating
- Cuisines

### Task 2
Extract the list of restaurants that have past event in the month of April 2019 and store the data as restaurant_events.csv.
- Event Id
- Restaurant Id
- Restaurant Name
- Photo URL
- Event Title
- Event Start Date
- Event End Date

### Task 3
From the dataset (restaurant_data.json), determine the threshold for the different rating text based on aggregate rating. Return aggregates for the following ratings only:
- Excellent
- Very Good
- Good
- Average
- Poor

## Pre-requisites
The following packages are used:
- Pandas
``` pandas
pip install pandas
```
- Numpy
``` numpy
pip install numpy
```
- JSON
``` numpy
pip install simplejson
```


## Installation
1. Clone the repository
```
git clone https://github.com/lwtn/GDS-CC4.0.git
```
2. Install the required packages (if needed)
3. Run restaurant.py

## Assumptions
1. Ratings are in the range of [0,5]







