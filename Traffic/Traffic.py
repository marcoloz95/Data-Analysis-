#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 23:13:47 2023

@author: marco
"""
import pandas as pd
from plotnine import *
import matplotlib.pyplot as plt
from datetime import datetime, time


# Open the JSON file
alerts = pd.read_json('alerts-processed.json')
jams = pd.read_json('jams-processed.json')

#%% DATA CLEANING (DONE)

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


#%% FIRST DAY ANALYSIS

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

#%% JAMS + FIRST DAY MAP COMPARISON 

plt.scatter(jams['x'], jams['y'], marker='o', label="Jams Full Data", color='red')

plt.scatter(first_day['x'], first_day['y'], marker='o', label='First Day Data', color='blue')

# Add labels, title, and legend
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Combined Scatterplot')
plt.legend()


#%% FIRST HOUR ANALYSIS 

first_hour = first_day.loc[(first_day['hour'] == 15)].drop_duplicates(subset='uuid') #filtered for unique uuid's 

first_hour.plot.scatter(x='x', y='y', marker='o', title='Coordinates Scatterplot')

#%% JAMS + FIRST DAY + FIRST HOUR COMPARISON 

plt.scatter(jams['x'], jams['y'], marker='o', label="Jams Full Data", color='orange')


plt.scatter(first_day['x'], first_day['y'], marker='o', label='First Day Full Data', color='red')

plt.scatter(first_hour['x'], first_hour['y'], marker='o', label='3PM Data', color='blue')

# Add labels, title, and legend
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.title('Combined Scatterplot')
plt.legend()




#%%




