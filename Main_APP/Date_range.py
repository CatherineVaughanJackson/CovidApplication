import pandas as pd

global County_options
global Year_options
global Month_options
global Day_options

#DROPDOWN MENUS

df_data=pd.read_csv("specimenDate_ageDemographic-unstacked.csv", parse_dates = ["date"])

County_options =df_data["areaName"].unique()
County_options.sort()

Date_options =df_data["date"].unique()
Date_options.sort()

Year_options =df_data["date"].dt.year.unique()

Month_options =df_data["date"].dt.month.unique()
Month_options.sort()

Day_options =df_data["date"].dt.day.unique()
Day_options.sort()