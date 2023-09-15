#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 16:15:04 2023

@author: marco
"""

import pandas as pd #always the first step
chipo_data = pd.read_csv("Chipo data 2_Usar.csv") #alwats make sure you're in the working directory 

#1. have a look to the first 10 entries. What are the data about?
chipo_data.head(10)

#2. How many observations do we have in the data?
chipo_data.describe() 

#3. What is the number of columns in the dataset? Print the name of all columns
chipo_data.columns

#4. #5. Which is the most repeated item? How many times does this item appear?
repeated = chipo_data.sort_values(by = "item_name", ascending=0)

repeated.item_name.value_counts() #first sorted the data frame based on item_name, then used value_counts to count the number of appearances per item

# or 

items_orders = chipo_data.item_name.value_counts()

#6. How many items were ordered in total?

chipo_data.quantity.sum()

#7. How many orders were made in the period? 

chipo_data.shape

#8. How many different items are sold?

unique = chipo_data.item_name.drop_duplicates()

#or 
 
chipo_data['item_name'].nunique()
