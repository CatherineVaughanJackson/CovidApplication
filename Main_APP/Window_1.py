#!/usr/bin/env python
# coding: utf-8

# In[3]:


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


# In[2]:


#*****WINDOW COMPARE AREAS CUMATIVLEY OR DAILY OVER TIME SPAN***

class Window1(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        
        self.title("Covid Data Visulisation Interface")
        self.configure(background = "grey22")
        self.iconbitmap("coronavirus_orange_right_HPY_2.ico")
        
        self.create_widget()
        self.create_title()
        self.load_data()
    
    
    def load_data(self):
        
        #LOADS DATA AS WINDOW IS OPENED
        global df_daily
        
        df_covid = pd.read_csv("specimenDate_ageDemographic-unstacked.csv", parse_dates=['date'])
        df_daily = df_covid[['areaName', 'date',"newCasesBySpecimenDate-0_59","newCasesBySpecimenDate-60+"]].copy()
        df_daily["Total_Cases"] = df_daily["newCasesBySpecimenDate-0_59"] + df_daily["newCasesBySpecimenDate-60+"]
        df_daily.drop_duplicates(inplace = True)
        
        #CREATES A COLUMN SUMMING TOTAL CASES CUMATIVLY BY AREA
        df_daily["Cumlative"]=df_daily.groupby(["areaName"])["Total_Cases"].cumsum(axis = 0)
        
        #RETURNS SMALLER DATAFRAME WITH NEW COLUMNS TOTAL AND CUMLATIVE
        return df_daily  
    
    
#****MAIN BUTTON SELECTION SECTION***    
    
    def daily_figure(self):
        #CHECKS TO SEE IF BOTH COUNTY OPTIONS ARE SELECTED TO DECIDE WHAT TYPE OF GRAPH
        self.area_choice("Total_Cases", df_daily)
    
    
    def cumalative_figure(self):

        #CHECKS TO SEE IF BOTH COUNTY OPTIONS ARE SELECTED TO DECIDE WHAT TYPE OF GRAPH
        self.area_choice("Cumlative", df_daily)
            
    
    
#***FURTHER PROCESSING SECTION***
    
    def area_choice(self, y_axis, dataframe):
        global df_total
        global df_total2
        
        #NARROWS DATAFRAME BASED ON AREA
        #CHECKS IF ONE OF COUNTY VARIBLES ARE EMPTY IT BOTH FULL MAKES DOUBLE FIGURE
        #IF ONLY ONE OPTION IS SELECTED DATAFRAME IS PROCESED BY AREA 
        #ONCE DATAFRAME IS NARROWED BY AREA, DATE RANGE FUNCTION APPLIED
        #THEN MAKE GRAPH FUNCTION
        #IF NEITHER AREA OPTION FILLED ERROR APPEARS
        
        if len(self.var0.get()) == 0 and len(self.var7.get()) == 0:
            messagebox.showinfo("error", "please select at least one area")
            return
        
        elif  len(self.var7.get()) == 0: 
            
            area = self.var0.get()
            df_area = dataframe[dataframe["areaName"]== area].copy()
            
            #AFTER AREA SELECTED DATE_RANGE SELECTED
            df_total = self.date_range(df_area)
            
            #IF ERROR HAS OCCURED IN DATE RANGE DATAFRAME EXIT LOOP
            if error == "yes":
                pass
            else:
                self.make_single_figure(y_axis, area, df_total)
            
        elif len(self.var0.get()) == 0:
            area = self.var7.get()
            df_area = dataframe[dataframe["areaName"]== area].copy()
            
            #AFTER AREA SELECTED DATE_RANGE SELECTED
            df_total = self.date_range(df_area)
            #IF ERROR HAS OCCURED IN DATE RANGE DATAFRAME EXIT LOOP
            if error == "yes":
                pass
            else:
                self.make_single_figure(y_axis, area, df_total)
        
        #IF BOTH OPTIONS ARE FILLED DOUBLE FIGURE FUNCTION IS RUN
        else:
            area1 = self.var0.get()
            area2 = self.var7.get()
            df_area1 = dataframe[dataframe["areaName"]== area1].copy()
            df_area2 = dataframe[dataframe["areaName"]== area2].copy()
            
            #NARROW DATAFRAME TO DATE RANGE
            df_total = self.date_range(df_area1)
            df_total2 =self.date_range(df_area2)
                #IF ERROR HAS OCCURED IN DATE RANGE DATAFRAME EXIT LOOP
            if error == "yes":
                pass
            else:
                self.make_double_figure(y_axis, area1, area2, df_total, df_total2)


    
    def date_range(self, dataframe):
        
        #RETURNS NARROWED DATAFRAME BASED ON TIME FRAME
        global error
        
            
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
                message = "please select date between" + str(min(dataframe["date"])) + " and " + str(max(dataframe["date"]))
                messagebox.showwarning(title ="error", message = message)
                error = "yes"

            elif end_date_dtype > max(dataframe["date"]):
                messagebox.showwarning(title ="error", message = message)
                error = "yes"

            else:
                time_range = (dataframe['date'] > start_date_dtype) & (dataframe['date'] <= end_date_dtype)
                df_date=dataframe.loc[time_range]
                error = ""
                return df_date
        except:
            messagebox.showwarning(title ="error", message = "please make sure all date entries are selected")
            error = "yes"
   

    
    
#****GRAPH PRODUCTION SECTION***
            
    def make_single_figure(self, y_axis,area, dataframe):
        
        #REMOVE GLOBAL IF CANVAS FUNCTION IS REMOVED
        
        figure1 = plt.figure(figsize = (5,5), dpi = 100)
        ax1=figure1.add_subplot(111)
        
        
        dataframe.plot(kind= "line",y=y_axis, x="date", ax=ax1)
        ax1.set(xlabel = "Date", ylabel = "Number of Cases per Day")
        
        
        #DEPENDING ON WHETHER CUMALTIVE OF DAILY BUTTON IS PRESSED CHANGES TITLE
        if y_axis == "Cumlative":
            ax1.set_title(y_axis +' Number of Cases per Day in ' + area)
        else:
            ax1.set_title('Number of Cases per Day in ' + area)
       
        figure1.tight_layout()   
        self.figure_on_canvas(figure1)

        
   
    def make_double_figure(self, y_axis, area1, area2, dataframe1, dataframe2):
        
        
        #FIGURE IS MADE WITH DOUBLE PLOT
        
        figure2 = Figure()
        plt.tight_layout()
        plt.style.use("ggplot")
    
        figure2,(ax1, ax2)=plt.subplots(nrows = 1, ncols = 2, sharey=True, figsize=(7,5)) 
        
        #DEPENDING ON WHETHER CUMALTIVE OF DAILY BUTTON IS PRESSED CHANGES TITLE
        
        if y_axis == "Cumlative":
            figure2.suptitle(y_axis +'Number of Cases per Day in ' + area1 +" and " + area2)
        else:
            figure2.suptitle('Number of Cases per Day in ' + area1 +" and " + area2)        
        
        
        #EACH DATAFRAME IS PLOTED
        
        dataframe1.plot(kind= "line",y=y_axis, x="date", ax=ax1)
        ax1.set(title = area1, ylabel = "Number of cases per Day", xlabel = "Date")

        dataframe2.plot(kind= "line",y=y_axis, x="date", ax=ax2)
        ax2.set(title = area2, xlabel = "Date")
        
        figure2.tight_layout() 
        self.figure_on_canvas(figure2)
        

    
    def figure_on_canvas(self,figure):
        
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().grid(column = 3, row = 1, rowspan = 10, padx =20, pady= 10)
        canvas.draw()

    
    
#***FORMATING SECTION***
    
    
    def create_title(self):
          
        border_color = tk.Frame(self,background="gold2")
        headerlabel = tk.Label(border_color, text = "Number of Covid cases by area over time"
                                                 " \n Please select an option, to select one area leave second area empty:",bg = "grey30", relief = "solid", fg = "white", font=("Arial", 24, "bold"))
        
        border_color.grid( column= 0, row = 0,columnspan = 4,padx =20, pady= 10, sticky = "nesw")
        headerlabel.grid( column= 0, row = 0, columnspan=4,padx =3, pady= 3, sticky = "nesw")
    
    
    def clear_box(self):
        #FUNCTION TO EMPTY SECOND COUNTY VARIBLE WHEN BUTTON IS PRESSED
        self.var7.set("")
    
    
    def create_widget(self):
        
        #MENU OPTION VARIABLES 
        self.var0 = tk.StringVar()
        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()
        self.var3 = tk.StringVar()
        self.var4 = tk.StringVar()
        self.var5 = tk.StringVar()
        self.var6 = tk.StringVar()
        self.var7 = tk.StringVar()
        
        
        #FORMATING DICTONARIES
        
        formating_colour = {"bg" : "grey32","relief" : "raised", "fg": "white", "font":("Arial", 15)}
        formating_position = { "padx":40, "pady" :10, "sticky" :"nesw"}

        
        
        #AREA LABELS AND OPTIONS
        county_label = tk.Label(self,  text='Select an Area:', **formating_colour)
        county_label.grid(column=0, row=1, **formating_position)
        
        county_option = tk.OptionMenu(self,self.var0, ti.County_options[0], *ti.County_options)
        county_option.grid(column=1, row=1, **formating_position)
        
        county_label2 = tk.Label(self,  text='Select a second Area:', **formating_colour)
        county_label2.grid(column=0, row=2, **formating_position)
        
        county_option2 = tk.OptionMenu(self,self.var7, ti.County_options[0], *ti.County_options)
        county_option2.grid(column=1, row=2, **formating_position)
        
        
        
        #BUTTON TO REMOVE SECOND AREA
        
        remove_county_option2 = tk.Button(self,text="Remove Second Area",bg="sky blue", command = lambda: self.clear_box())
        remove_county_option2.grid(column=0, row=9, **formating_position)
        
        
        
        #START DATE LABELS AND OPTION MENUS
        
        sday_label = tk.Label(self,  text='Select a start day:', **formating_colour)
        sday_label.grid(column=0, row=3, **formating_position)
        
        sday_option = tk.OptionMenu(self,self.var1, *ti.Day_options)
        sday_option.grid(column=1, row=3, **formating_position)
        
        smonth_label = tk.Label(self,  text='Select a start Month:',  **formating_colour)
        smonth_label.grid(column=0, row=4,**formating_position)
        
        smonth_option = tk.OptionMenu(self,self.var2,  *ti.Month_options)
        smonth_option.grid(column=1, row=4, **formating_position)
        
        syear_label = tk.Label(self,  text='Select a start Year:',  **formating_colour)
        syear_label.grid(column=0, row=5,**formating_position)
        
        syear_option = tk.OptionMenu(self,self.var3, *ti.Year_options)
        syear_option.grid(column=1, row=5, **formating_position)

        
        
        #END DATE LABEL AND OPTIONS MENUS
        
        eday_label = tk.Label(self,  text='Select an end day:',  **formating_colour)
        eday_label.grid(column=0, row=6,**formating_position)
        
        eday_option = tk.OptionMenu(self,self.var4,  *ti.Day_options)
        eday_option.grid(column=1, row=6, **formating_position)
        
        emonth_label = tk.Label(self,  text='Select an end Month:',  **formating_colour)
        emonth_label.grid(column=0, row=7,**formating_position)
        
        emonth_option = tk.OptionMenu(self,self.var5, *ti.Month_options)
        emonth_option.grid(column=1, row=7, **formating_position)

        eyear_label = tk.Label(self,  text='Select an end year:',  **formating_colour)
        eyear_label.grid(column=0, row=8,**formating_position)
        
        eyear_option = tk.OptionMenu(self,self.var6, *ti.Year_options)
        eyear_option.grid(column=1, row=8, **formating_position)
        
        
        
        #GRAPH DISPLAY BUTTONS AND QUIT 
        
        display_button = tk.Button(self,  text='Show Daily Graphical Display', command=lambda: self.daily_figure() )  
        display_button.grid(column = 1, row =9, **formating_position)
        
        cumalative_button = tk.Button(self,  text='Show Cumalative Graphical Display', command=lambda: self.cumalative_figure() )  
        cumalative_button.grid(column = 1, row =10, **formating_position)        
        
        quit = tk.Button(self, bg= "red",text = "QUIT", command = self.destroy)
        quit.grid(column = 0, row =10, **formating_position)


# In[ ]:




