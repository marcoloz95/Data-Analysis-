#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 23:13:47 2023

@author: marco
"""

import pandas as pd
from plotnine import *
from sklearn.cluster import KMeans
from sklearn import preprocessing #necessary to re-label the descriptive columns
import matplotlib.pyplot as plt
from datetime import datetime, time


# Open the JSON file
alerts = pd.read_json('alerts-processed.json')
jams = pd.read_json('jams-processed.json')

#%% DATA CLEANING 

# Convert 'datetime' column to pandas-compatible datetime format, and convert to string for further analysis 
alerts['pubMillis'] = pd.to_datetime(alerts['pubMillis'], unit='ms') #this line converts the pubmillis column into a more readable format 

alerts['date'] = alerts['pubMillis'].dt.date #this line extracts the date item from the pubMillis column, and stores it into a new column called 'Date'

alerts['time'] = alerts['pubMillis'].dt.time #same as the above but for the time aspect 

alerts['date'] = alerts['date'].astype(str) #this converts the column rows into strings 

#same process executed below for the jams file

jams['pubMillis'] = pd.to_datetime(jams['pubMillis'], unit='ms')

jams['date'] = jams['pubMillis'].dt.date

jams['time'] = jams['pubMillis'].dt.time

jams['date'] = jams['date'].astype(str)

jams['time'].dtype

jams['x'] = jams['line'].apply(lambda coords: [coord['x'] for coord in coords]) #extracts the x coordinates from the pubmillis column, into a list within a new column 'x'
jams['y'] = jams['line'].apply(lambda coords: [coord['y'] for coord in coords]) #same but for y 

jams['x'] = jams['x'].apply(lambda x: x[0] if isinstance(x, list) else x) #extracts the first value within column x
jams['y'] = jams['y'].apply(lambda y: y[0] if isinstance(y, list) else y) #same but for y 

jams.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot') #plots all of the coordinates together, for comparison later on 


#%%

#Start analysis of first date 

first_day = jams.loc[jams.date == '2017-07-08' , :] #select all the rows wherein the date within the james file corresponds to July 8, 2017, the first day within the set 
first_day = first_day.loc[:, ["time", 'uuid', "street", "speed", "delay", "x", "y"]] #filter for what we need 

# Plot all coordinates using pandas scatterplot
first_day.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot')

# Show the plot
plt.show()

# Convert the column to string type
first_day['time'] = first_day['time'].astype(str)

# Extract the hour from the time column using string manipulation
first_day.loc[:, 'hour'] = first_day['time'].str.slice(start=0, stop=2).astype(int)

first_day.hour.nunique()

#%% PER HOUR TRIAL 

first_hour = first_day.loc[(first_day['hour'] == 15)].drop_duplicates(subset='uuid') #filtered for unique uuid's 
#first_hour = first_hour.loc[:, ["hour", 'uuid', "street", "speed", "delay", "x", "y"]] 

# Flatten the 'coordinates' column
#df = first_hour.explode('x','y')

# Separate the flattened coordinates into 'x' and 'y' columns
#first_hour[['x', 'y']] = pd.DataFrame(first_hour['coordinates'].tolist(), index=df.index)

# Flatten the 'x' and 'y' columns
first_hour = first_hour.explode('x')
first_hour = first_hour.explode('y')

first_hour['x'] = first_hour['line'].apply(lambda coords: [coord['x'] for coord in coords])
first_hour['y'] = first_hour['line'].apply(lambda coords: [coord['y'] for coord in coords])


first_hour['x'] = first_hour['x'].apply(lambda x: x[0] if isinstance(x, list) else x)
first_hour['y'] = first_hour['y'].apply(lambda y: y[0] if isinstance(y, list) else y)

#grouped_data = first_hour.groupby(['hour', 'street', 'x', 'y'])['speed', 'delay'].mean().reset_index()

# Create a single DataFrame to store all coordinates 
first_hour_coordinates = pd.DataFrame()

for _, row in first_hour.iterrows():
    coordinates = pd.DataFrame({'x': [row['x']], 'y': [row['y']]})
    first_hour_coordinates = pd.concat([first_coordinates, coordinates], ignore_index=True)

# Plot all coordinates using pandas scatterplot

first_hour.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot')

# Show the plot
plt.show()

#%%

first_coordinates.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot')

first_hour.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot')


# Create a scatterplot for 'first_coordinates' with one color
plt.scatter(first_coordinates['x'], first_coordinates['y'], marker='o', label='First Coordinates', color='blue')

plt.scatter(jams['x'], jams['y'], marker ='o', label='Total Coordinates', color='blue')

# Create a scatterplot for 'first_hour' with another color
plt.scatter(first_hour['x'], first_hour['y'], marker='o', label='First Hour', color='red')

# Add labels, title, and legend
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Combined Scatterplot')
plt.legend()

# Show the plot
plt.show()

jams.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot')





#%%

#show the coordinates per hour?

selected_rows = first.loc[(first['hour'] >= 15) & (first['hour'] <= 19)]

selected_rows['x'] = selected_rows['line'].apply(lambda coords: [coord['x'] for coord in coords])
selected_rows['y'] = selected_rows['line'].apply(lambda coords: [coord['y'] for coord in coords])

firsthour = selected_rows.loc[:, ["hour", "street", "speed", "delay", "x", "y"]]

firsthour['x'] = firsthour['x'].apply(lambda x: x[0] if isinstance(x, list) else x)
firsthour['y'] = firsthour['y'].apply(lambda y: y[0] if isinstance(y, list) else y)

grouped_data = firsthour.groupby(['hour', 'street', 'x', 'y'])['speed', 'delay'].mean().reset_index()

first_coordinates_time = pd.DataFrame()

for _, row in firsthour.iterrows():
    coordinates = pd.DataFrame({'x': [row['x']], 'y': [row['y']]})

    all_coordinates1 = pd.concat([all_coordinates1, coordinates], ignore_index=True)

# Plot all coordinates using pandas scatterplot
all_coordinates1.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot')
first_coordinates_time.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot')


# Show the plot
plt.show()

#%%

#A plot of all the coordinates provided in the dataset 

jams['x'] = jams['line'].apply(lambda coords: [coord['x'] for coord in coords])
jams['y'] = jams['line'].apply(lambda coords: [coord['y'] for coord in coords])

all_coordinates = pd.DataFrame(columns=['x', 'y'])

# Loop through the rows and extract the coordinates
for _, row in jams.iterrows():
    coordinates = pd.DataFrame(row['line'])
    all_coordinates = pd.concat([all_coordinates, coordinates], ignore_index=True)

# Plot all coordinates using pandas scatterplot
all_coordinates.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot')

# Show the plot
plt.show()


#%% GPT 

first = jams.loc[jams.date == '2017-07-08', :]  # Select all rows with the date '2017-07-08' from the 'jams' DataFrame.

# Extract 'x' coordinates from the 'line' column and store them in a new 'x' column.
first['x'] = first['line'].apply(lambda coords: [coord['x'] for coord in coords])

# Extract 'y' coordinates from the 'line' column and store them in a new 'y' column.
first['y'] = first['line'].apply(lambda coords: [coord['y'] for coord in coords])

# Create an empty DataFrame to store all coordinates.
first_coordinates = pd.DataFrame(columns=['x', 'y'])

# Loop through the rows and extract the coordinates, then concatenate them.
for _, row in first.iterrows():
    coordinates = pd.DataFrame(row['line'])
    first_coordinates = pd.concat([first_coordinates, coordinates], ignore_index=True)

# Plot all coordinates using a pandas scatterplot.
first_coordinates.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot')

# Show the plot.
plt.show()

# Convert the 'time' column to string type.
first['time'] = first['time'].astype(str)

# Extract the hour from the 'time' column using string manipulation.
first['hour'] = first['time'].str.slice(start=0, stop=2).astype(int)

# Count the number of unique hours.
unique_hours = first['hour'].nunique()

# Select rows where the hour is between 15 and 19 (3 PM to 7 PM).
selected_rows = first.loc[(first['hour'] >= 15) & (first['hour'] <= 19)]

# Extract 'x' and 'y' coordinates from the 'line' column.
selected_rows['x'] = selected_rows['line'].apply(lambda coords: [coord['x'] for coord in coords])
selected_rows['y'] = selected_rows['line'].apply(lambda coords: [coord['y'] for coord in coords])

# Create a DataFrame containing selected columns.
first_hour = selected_rows.loc[:, ["hour", "street", "speed", "delay", "x", "y"]]

# Ensure 'x' and 'y' columns contain single values (not lists).
first_hour['x'] = first_hour['x'].apply(lambda x: x[0] if isinstance(x, list) else x)
first_hour['y'] = first_hour['y'].apply(lambda y: y[0] if isinstance(y, list) else y)

# Group and calculate the mean of 'speed' and 'delay' by hour, street, 'x', and 'y'.
grouped_data = first_hour.groupby(['hour', 'street', 'x', 'y'])['speed', 'delay'].mean().reset_index()

# Create an empty DataFrame to store coordinates.
first_coordinates_time = pd.DataFrame()

# Loop through the rows and extract coordinates, then concatenate them.
for _, row in first_hour.iterrows():
    coordinates = pd.DataFrame({'x': [row['x']], 'y': [row['y']]})
    first_coordinates_time = pd.concat([first_coordinates_time, coordinates], ignore_index=True)

# Plot all coordinates using pandas scatterplots.
all_coordinates1.plot.scatter(x='x', y='y', marker='o', title='All Coordinates Scatterplot')
first_coordinates_time.plot.scatter(x='x', y='y', marker='o', title='Coordinates by Time Scatterplot')

# Show the plots.
plt.show()



