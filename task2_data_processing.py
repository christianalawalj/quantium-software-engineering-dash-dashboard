import csv
import glob
import os
import pandas as ps

#1/ first read from each csv file line by line. in data
data0 = ps.read_csv('data/daily_sales_data_0.csv')
data1 = ps.read_csv('data/daily_sales_data_1.csv')
data2 = ps.read_csv('data/daily_sales_data_2.csv')
#now combine the files into one table :
datatogether = [data0, data1, data2]
datatable = ps.concat(datatogether, ignore_index= True)

#find all the products in the datatable and force them to become a string, and then for each string strip extra spaces
datatable["product"] = datatable["product"].astype(str).str.strip()
#in the big table keep only the rows where the product name is pink morsel and then copy it into that variable
pinkMorselsOnly = datatable[datatable["product"] == "pink morsel"].copy()

#Convert the price into string to remove $ and then back to a floating number remember also for each str in price remove space
pinkMorselsOnly["price"] = pinkMorselsOnly["price"].astype(str).str.replace("$", "",  regex = False)
#take the newly converted strings price values in the pink morsel table and convert it into a
pinkMorselsOnly["price"] = pinkMorselsOnly["price"].astype(float)

pinkMorselsOnly["quantity"] = ps.to_numeric(pinkMorselsOnly["quantity"], errors='coerce')
pinkMorselsOnly["sales"] = pinkMorselsOnly["quantity"] * pinkMorselsOnly["price"]
final_output = pinkMorselsOnly[["sales", "date", "region"]].copy()

#save to a csv file
final_output["date"] = ps.to_datetime(final_output["date"])
final_output = final_output.sort_values(by=["date"], ascending=False)
final_output.to_csv("outputfile.csv", index = False)
print(" Done! Created outputfile.csv")
print(final_output.head())

