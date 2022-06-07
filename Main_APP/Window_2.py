#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from datetime import datetime

get_ipython().run_line_magic('matplotlib', 'qt')

import Geography_lists as Geo
import Date_range as ti
from PIL import ImageTk, Image
from tkinter import messagebox


# In[ ]:


#******* AREAS WITH THE HIGHEST NUMBER OF COVID CASES BY TIME (REGION, CITIES, COUNTIES)******

class Window2(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Covid Data Visulisation Interface")
        self.configure(background = "grey22")
        self.iconbitmap("coronavirus_orange_right_HPY_2.ico")
        
        self.create_widget()
        self.create_title()
        self.load_data()

   
    #***PRE-PROCESSING SECTION***
    
    def load_data(self):
        
        global df_daily
        
        #LOAD IN THE DATAFRAME AS SOON AS WINDOW OPENS REDUCE COLUMNS TO ONLY REQUIRED
        #IF GRAPH IS CHANGED MAIN DATA IS NOT RELOADED
        
        df_covid = pd.read_csv("specimenDate_ageDemographic-unstacked.csv", parse_dates=['date'])
        df_daily = df_covid[['areaName', 'date',"newCasesBySpecimenDate-0_59","newCasesBySpecimenDate-60+"]].copy()
        df_daily["Total_Cases"] = df_daily["newCasesBySpecimenDate-0_59"] + df_daily["newCasesBySpecimenDate-60+"]
        df_daily.drop_duplicates(inplace = True)
        
        #RETURNS SMALLER DATAFRAME
        return df_daily    
    
    #***MAIN BUTTON OPTION CHOICE SECTION***
        
    def city_figure(self): 
        
        #UNWANTED AREAS REMOVED FROM DATAFRAME
        city_string = "|".join(Geo.Counties)
        df_daily2=df_daily[df_daily["areaName"].str.contains(city_string)==True].copy()
        
        #NARROW DATAFRAME USING DATE FUNCTION
        df_date = self.date_range(df_daily2)
        
        if error == "yes":
            pass
        else:
            #NARROWED DATAFRAME THEN SUMS TOTAL CASES BY AREA
            df_total = self.group_by(df_date)

            #FINAL FIGURE MADE
            self.make_figure(df_total)
    
    def county_figure(self):       
        
        #UNWANTED AREAS REMOVED
        county_string = "|".join(Geo.Cities_Towns)
        df_daily2=df_daily[df_daily["areaName"].str.contains(county_string)==True].copy()
        
        #NARROW DATAFRAME USING DATE FUNCTION
        df_date =self.date_range(df_daily2)
        
        if error == "yes":
            pass
        else:
            #NARROWED DATAFRAME THEN SUMS TOTAL CASES BY AREA
            df_total =self.group_by(df_date)

            #FINAL FIGURE MADE
            self.make_figure(df_total)
        
    def region_figure(self):       
        
        #UNWANTED AREAS REMOVED
        region_string = "|".join(Geo.Region)
        df_daily2=df_daily[df_daily["areaName"].str.contains(region_string)==True].copy()
        
        #NARROW DATAFRAME USING DATE FUNCTION
        df_date=self.date_range(df_daily2)
        
        if error == "yes":
            pass
        else:
            #NARROWED DATAFRAME THEN SUMS TOTAL CASES BY AREA
            df_total =self.group_by(df_date)

            #FINAL FIGURE MADE
            self.make_figure(df_total)
    
        
    
#***FUTHER PROCESSING SECTION***
    
    
    def date_range(self,dataframe):

        global error
        #NARROWS DATAFRAME TO PRESELECTED DATES
        
            
        start_day= self.var1.get()
        start_day = int(start_day) -1
        start_month= self.var2.get()
        start_year= self.var3.get()
        end_day= self.var4.get()
        end_month= self.var5.get()
        end_year= self.var6.get()
        
        start_date = str(start_year) +"-" + str(start_month) + "-" + str(start_day)
        end_date = str(end_year) +"-" + str(end_month) + "-" + str(end_day)
        
        try:
            start_date_dtype = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_dtype = datetime.strptime(end_date, "%Y-%m-%d") 

            if start_date_dtype >= end_date_dtype:
                messagebox.showwarning(title ="error", message = "please make sure start date is before end date")
                error = "yes"

            elif start_date_dtype < min(dataframe["date"]):
                message = "please select date between" + str(min(dataframe["date"])) + "and" + str(max(dataframe["date"]))
                messagebox.showwarning(title ="error", message = message)
                error = "yes"

            elif end_date_dtype > max(dataframe["date"]):
                messagebox.showwarning(title ="error", message = message)
                error = "yes"

            else:
                time_range = (dataframe['date'] > start_date_dtype) & (dataframe['date'] <= end_date_dtype)
                df_date=dataframe.loc[time_range]
                error = ""
                 #RETURNS DATAFRAME IN NARROW DATE RANGE
                return df_date
        except:
            messagebox.showwarning(title ="error", message = "please make sure all date entries are selected")
            error = "yes"
       


    def group_by(self,dataframe):

        
        #DATAFRAME WITH DATE RANGE APPLIED HAS TOTAL COVID CASES SUMMED BASED ON AREA
        df_area =dataframe.groupby('areaName')[["Total_Cases"]].sum()
        df_area["areaName"]=df_area.index
        
        #SORTS DATAFRAME TO MOST CASES TO TOP
        df_area.sort_values(by=["Total_Cases"], ascending=False, inplace = True)
        
        #RETURNS DATAFRAME OF TOTAL CASES PER AREA BY DATE RANGE SELECTED
        return df_area
    
    
    

    
    #***FINAL FIGURE PRODUCTION SECTION***
    
    def make_figure(self,dataframe):
        
        #FIGURE PLOTTED
        figure1,ax=plt.subplots()
        
        plt.style.use("ggplot")
        
        #TOP 10 IN DATAFRAME PLOTTED
        dataframe.head(10).plot(kind= "bar",y="Total_Cases", x="areaName", ax=ax)
        ax.set(title = "Total number of cases over time by Area", xlabel = "Area")
        
        figure1.tight_layout()
        
        #PLOTTED GRAPH INSERTED TO TKINTER FRAME
        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.draw()
        canvas.get_tk_widget().grid(column = 3, row = 1, rowspan = 9, padx =40, pady= 40)
    
    
    
    
    #***FORMATING SECTION***
    
    def create_title(self):
          
        #TITLE AND BORDER FORMATED AND PLACED ON GRID
        
        border_color = tk.Frame(self,background="gold2")
        headerlabel = tk.Label(border_color, text = "Areas with the most confirmed Covid cases"
                                                 " \n by Region, Cities and Towns or County:",bg = "grey30", relief = "solid", fg = "white", font=("Arial", 24, "bold"))
        
        border_color.grid( column= 0, row = 0,columnspan = 4,padx =20, pady= 10, sticky = "nesw")
        headerlabel.grid( column= 0, row = 0, columnspan=4,padx =3, pady= 3, sticky = "nesw")
    
    
    def create_widget(self):
        
        #VARIABLES FOR DROP DOWN MENUS
        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()
        self.var3 = tk.StringVar()
        self.var4 = tk.StringVar()
        self.var5 = tk.StringVar()
        self.var6 = tk.StringVar()
        
        
        #FORMATING DICTONARIES
        
        formating_colour = {"bg" : "grey32","relief" : "raised", "fg": "white", "font":("Arial", 15)}
        formating_position = { "padx":40, "pady" :10, "sticky" :"nesw"}

        
        #START LABELS AND OPTION MENUS
        
        sday_label = tk.Label(self,  text='Select a start day:', **formating_colour)
        sday_label.grid(column=0, row=1, **formating_position)
    
        sday_option = tk.OptionMenu(self,self.var1, *ti.Day_options)
        sday_option.grid(column=1, row=1, **formating_position)
        
        smonth_label = tk.Label(self,  text='Select a start Month:',  **formating_colour)
        smonth_label.grid(column=0, row=2,**formating_position)
        
        smonth_option = tk.OptionMenu(self,self.var2,  *ti.Month_options)
        smonth_option.grid(column=1, row=2, **formating_position)
        
        syear_label = tk.Label(self,  text='Select a start Year:',  **formating_colour)
        syear_label.grid(column=0, row=3,**formating_position)
        
        syear_option = tk.OptionMenu(self,self.var3, *ti.Year_options)
        syear_option.grid(column=1, row=3, **formating_position)

        
        #END LABELS AND OPTION MENUS
        
        eday_label = tk.Label(self,  text='Select an end day:',  **formating_colour)
        eday_label.grid(column=0, row=4,**formating_position)
        
        eday_option = tk.OptionMenu(self,self.var4,  *ti.Day_options)
        eday_option.grid(column=1, row=4, **formating_position)
        
        emonth_label = tk.Label(self,  text='Select an end Month:',  **formating_colour)
        emonth_label.grid(column=0, row=5,**formating_position)
        
        emonth_option = tk.OptionMenu(self,self.var5, *ti.Month_options)
        emonth_option.grid(column=1, row=5, **formating_position)

        eyear_label = tk.Label(self,  text='Select an end year:',  **formating_colour)
        eyear_label.grid(column=0, row=6,**formating_position)
        
        eyear_option = tk.OptionMenu(self,self.var6, *ti.Year_options)
        eyear_option.grid(column=1, row=6, **formating_position)
        
        
        #DISPLAY AND QUIT BUTTONS 
        
        City_button = tk.Button(self,  text='Show Confirmed Cases by City/Town', command=lambda: self.city_figure() )  
        City_button.grid(column = 1, row =7, **formating_position)
        
        County_button = tk.Button(self,  text='Show Confirmed Cases by County', command=lambda: self.county_figure() )  
        County_button.grid(column = 1, row =8, **formating_position)
        
        region_button = tk.Button(self,  text='Show Confirmed Cases by Region', command=lambda: self.region_figure() )  
        region_button.grid(column = 1, row =9, **formating_position) 
        
        quit = tk.Button(self, bg= "red",text = "QUIT", command = self.destroy)
        quit.grid(column = 0, row =9, **formating_position)

