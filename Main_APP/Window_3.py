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


#*****UK TOTALS CASES AND PERCENTAGE CHANGES*****
class Window3(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Covid Data Visulisation Interface")
        self.configure(background = "grey22")
        #self.attributes("-fullscreen", True)
        self.iconbitmap("coronavirus_orange_right_HPY_2.ico")
        
        self.create_widget()
        self.create_title()
        self.load_data()

#****PRE-PROCESSING SECTION*****
    def load_data(self):
        
        global df_daily
        
        df_covid = pd.read_csv("specimenDate_ageDemographic-unstacked.csv", parse_dates=['date'])
        df_daily = df_covid[['areaName', 'date',"newCasesBySpecimenDate-0_59","newCasesBySpecimenDate-60+"]].copy()
        df_daily["Total_Cases"] = df_daily["newCasesBySpecimenDate-0_59"] + df_daily["newCasesBySpecimenDate-60+"]
        df_daily = df_daily[df_daily["areaName"]== "United Kingdom"].copy()
        
        df_daily.drop_duplicates(inplace = True)
        df_daily["Cumlative"]=df_daily.groupby(["areaName"])["Total_Cases"].cumsum(axis = 0) 
       
        return df_daily

    
#****MAIN BUTTON SELECTION SECTION*****            
    def pct_figure_day(self):
        
        #NARROW DATAFRAME BY DATE
        df_date = self.date_range(df_daily)
        if error=="yes":
            pass
        else:
            #IF NO ERROR THEN CALCULATE DAILY PERCENTAGE CHANGE 
            self.percentage_change_calculation(df_date)
            self.create_figure("percentage_change"," day ", df_pct)
    
    def pct_figure_month(self):
        
        #SET DAY OPTIONS TO BEGINING OF MONTH
        #DOESN'T MATTER IF BOX IS EMPTY OR FULL
        #SET START DATE AS TWO AS DATE RANGE -1 FROM DATE TO AVOID 0 ERROR
        self.var1.set("2")
        self.var4.set("1")
        
        if self.var2.get() == self.var5.get():
            #MAKE SURE MONTHS ARE AT LEAST ONE MONTH APART
            messagebox.showwarning(title ="error", message = "please select dates at least one month apart")
        else:
            #NARROW DATAFRAME BY DATE
            df_date = self.date_range(df_daily)
            if error=="yes":
                pass
            else:
                #GROUPS DATES BY MONTH
                df_date1 = df_date.groupby(pd.Grouper(freq='M', key='date'))[['Total_Cases']].sum()
                df_date1["date"]=df_date1.index

                #THEN CALCULATES PERCENTAGE CHANGE
                self.percentage_change_calculation(df_date1)
                self.create_figure("percentage_change"," month ", df_pct)
            
    def cumlative_figure(self):
        
        #NARROWS DATAFRAME BY DATE
        df_date = self.date_range(df_daily)
        if error=="yes":
            pass
        else:
            #CUMLATIVE CALCULATION ALREADY DONE IN PREPROCESSING
            self.create_figure("Cumlative","month ", df_date)
    
    def total_by_month(self):
        
        #SET DAY OPTIONS TO BEGINING OF MONTH
        #DOESN'T MATTER IF BOX IS EMPTY OR FULL
        #SET START DATE AS TWO AS DATE RANGE -1 FROM DATE TO AVOID 0 ERROR
        self.var1.set("2")
        self.var4.set("1")
        
        if self.var2.get() == self.var5.get():
            messagebox.showwarning(title ="error", message = "please select dates at least one month apart")
        else:
            df_date = self.date_range(df_daily)
            if error=="yes":
                pass
            else:
                #SUM CASES BY MONTH
                df_date1 = df_date.groupby(pd.Grouper(freq='M', key='date'))[['Total_Cases']].sum()
                df_date1["date"]=df_date1.index
                self.create_figure("Total_Cases"," month ", df_date1)
    

    #****FURTHER-PROCESSING SECTION***

    def date_range(self, dataframe):

        global df_date
        global error
        #NARROWS DATAFRAME TO PRESELECTED DATES
        
            
        start_day= self.var1.get()
        start_day= int(start_day) -1
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
            messagebox.showwarning(title ="error", message = "please make sure all appropriate date entries are selected")
            error = "yes"
    
    def percentage_change_calculation(self, dataframe):
        
        global df_pct
        
        df_pct = dataframe.squeeze()
        df_pct=df_pct.copy()
        df_pct["percentage_change"]=df_pct["Total_Cases"].pct_change(fill_method = "bfill")
        df_pct["percentage_change"].replace([np.inf, -np.inf], np.nan, inplace = True)
        df_pct["percentage_change"].fillna(0, inplace = False)

        return df_pct
    

#****FIGURE CREATION SECTION*****

    def create_figure(self,y_axis,time,dataframe):

        figure1,ax=plt.subplots()
        dataframe.plot(kind= "line",y=y_axis, x="date", ax=ax)
        
        if y_axis == "percentage_change": 
            ax.set_title("percentage change by " + time + "in the UK")
            ax.axhline(y=0, linewidth= 0.2, color = "red")
        elif y_axis == "Total_Cases":
            ax.set_title("Total cases in the UK by Month")
        else:
            ax.set_title("Total Cumalitve case numbers in the UK over time")
        
        figure1.tight_layout()

        canvas = FigureCanvasTkAgg(figure1, self)
        canvas.draw()
        canvas.get_tk_widget().grid(column = 3, row = 1, rowspan = 9, padx =40, pady= 40)

        
        
#***FORMATING SECTION***
    def create_title(self):
          
        border_color = tk.Frame(self,background="gold2")
        headerlabel = tk.Label(border_color, text = "Covid cases in the UK "
                                                 " \n Please select an option:",bg = "grey30", relief = "solid", fg = "white", font=("Arial", 24, "bold"))
        
        border_color.grid( column= 0, row = 0,columnspan = 4,padx =20, pady= 10, sticky = "nesw")
        headerlabel.grid( column= 0, row = 0, columnspan=4,padx =3, pady= 3, sticky = "nesw")   
        

        
    def create_widget(self):
        
        #OPTION MENU VARIABLES
        
        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()
        self.var3 = tk.StringVar()
        self.var4 = tk.StringVar()
        self.var5 = tk.StringVar()
        self.var6 = tk.StringVar()

        #FORTMATTING
        
        formating_colour = {"bg" : "grey32","relief" : "raised", "fg": "white", "font":("Arial", 15)}
        formating_position = { "padx":40, "pady" :10, "sticky" :"nesw"}

        #START DATE LABELS AND OPTIONS
        
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

        #END DATE LABELS AND OPTIONS
        
        eday_label = tk.Label(self,  text='Select a end day:', **formating_colour)
        eday_label.grid(column=0, row=4, **formating_position)
    
        eday_option = tk.OptionMenu(self,self.var4, *ti.Day_options)
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
        
        daily_pct_button = tk.Button(self,  text='Show Percentage Change by Day', command=lambda: self.pct_figure_day() )  
        daily_pct_button.grid(column = 0, row =7, **formating_position)
        
        monthly_pct_button = tk.Button(self,  text='Show Percentage change by Month', command=lambda: self.pct_figure_month() )  
        monthly_pct_button.grid(column = 1, row =7, **formating_position)
        
        cumalative_button = tk.Button(self,  text='Show Cumlative Total', command=lambda: self.cumlative_figure() )  
        cumalative_button.grid(column = 0, row =8, **formating_position) 
        
        monthly_button = tk.Button(self,  text='Show Total UK Cases by Month', command=lambda: self.total_by_month() )  
        monthly_button.grid(column = 1, row =8, **formating_position)
        
        quit = tk.Button(self, bg= "red",text = "QUIT", command = self.destroy)
        quit.grid(column = 0, row =9, **formating_position)

