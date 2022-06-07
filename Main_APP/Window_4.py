#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
get_ipython().run_line_magic('matplotlib', 'qt')

from PIL import ImageTk, Image
from tkinter import messagebox

from datetime import date
import requests
import json


# In[ ]:


class Window4(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        
        self.title("Covid Data Visulisation Interface")
        self.configure(background = "grey22")
        
        self.iconbitmap("coronavirus_orange_right_HPY_2.ico")
        
        self.create_widget()
        self.create_title()


    
    def age(self):
        
        self.group_by(df_date,"age_range")
        self.make_figure(df_total,"age_range")    
 
    def gender(self):
        
        self.group_by(df_date,"gender" )
        self.make_figure(df_total,"gender")
    
    def ethnicity(self):
        
        self.group_by(df_date,"self_defined_ethnicity")
        self.make_figure(df_total,"self_defined_ethnicity")
    
    def reason(self):
        
        self.group_by(df_date,"object_of_search" )
        self.make_figure(df_total,"object_of_search")
    
    def load_data(self):
        
        #data can't be pre-loaded at the start as we need to know poilce force and date first
        global df_date

        
        if len(self.var2.get()) == 0:
            messagebox.showwarning(title ="error", message="please make sure a police force is selected ")
        else:
            police_force = self.var2.get()
            
            if len(self.var0.get()) == 0 or len(self.var1.get()) ==0:
                messagebox.showwarning(title ="error", message="please make sure both date options are filled ")
            else:
                
                Month =self.var0.get()
                Year=self.var1.get()

                date=str(Year)+"-"+str(Month)
                date_parameters = {"date": date}

                response = requests.get("https://data.police.uk/api/stops-force?force=" + police_force, params=date_parameters)

                if response.status_code > 400:
                    messagebox.showwarning(title ="error", message ="Error, Try selecting a date from the last 3 years, or check network connection")

                else:
                    items = []
                    for i in response.json():
                        items.append(i)
                    df_date = pd.DataFrame(items)


                    age_button["state"]="normal"
                    gender_button["state"]="normal"
                    ethnicity_button["state"]="normal"
                    reason_button["state"]="normal"
                    
                    reset_button["state"]="normal"
                    
                    month_option["state"]="disable"
                    year_option["state"]="disable"
                    police_option["state"]="disable"
                    load_button["state"]="disable"

                    return df_date
   
    def reset_data(self):
        
        month_option["state"]="normal"
        year_option["state"]="normal"
        police_option["state"]="normal"
        load_button["state"]="normal"
        
        age_button["state"]="disable"
        gender_button["state"]="disable"
        ethnicity_button["state"]="disable"
        reason_button["state"]="disable"
        
     
    
    def group_by(self, dataframe, x_axis):
        
        global df_total
        
        df_total = dataframe[[x_axis]].copy()
        df_total['freq'] = df_total.groupby(x_axis)[x_axis].transform('count').copy()
        df_total = df_total.drop_duplicates()
        df_total.dropna(inplace = True)
        df_total.sort_values("freq", axis = 0, ascending = False,
                 inplace = True)
        
        return df_total
    
    def make_figure(self,dataframe,x_axis):
        
        #FIGURE PLOTTED
        figure1,ax=plt.subplots()
        plt.style.use("ggplot")
       

        dataframe.plot(kind= "bar",y="freq", x=x_axis, ax=ax)
        ax.set_title("Total frequency by Month")
        plt.xticks(rotation=45)
        
        if x_axis == "self_defined_ethnicity":

            plt.xticks(fontsize=4, rotation =90)
        else:
            pass
        
        plt.tight_layout()
        
        
        #PLOTTED GRAPH INSERTED TO TKINTER FRAME
        canvas = FigureCanvasTkAgg(figure1, self)
        #canvas.draw()
        canvas.get_tk_widget().grid(column = 3, row = 1, rowspan = 7, padx =40, pady= 40)
    
    def get_police_names(self):
        
        df =pd.read_json ("https://data.police.uk/api/forces")
        police_names =df["id"].unique()    
        
        return police_names
    
    def get_todays_date(self):
        
        global months
        global years
        
        todays_date = date.today()
        
        this_year = todays_date.year
        years=[this_year, this_year -1, this_year -2,this_year -3]

        months=[i for i in range(1,13)]
        
        return months, years
                          
                          
    def create_title(self):

        #TITLE AND BORDER FORMATED AND PLACED ON GRID  
        border_color = tk.Frame(self,background="gold2")
        headerlabel = tk.Label(border_color, text = "Stop and Search data by Month "
                                                 " \n Please load data before selecting parameter for visualisation:",bg = "grey30", relief = "solid", fg = "white", font=("Arial", 24, "bold"))
                               

        border_color.grid( column= 0, row = 0,columnspan = 4,padx =20, pady= 10, sticky = "nesw")
        headerlabel.grid( column= 0, row = 0, columnspan=4,padx =3, pady= 3, sticky = "nesw") 
                          
                          
    def create_widget(self):

        #MENU OPTION VARIABLES 
        self.var0 = tk.StringVar()
        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()


        #FORMATING DICTONARIES

        formating_colour = {"bg" : "grey32","relief" : "raised", "fg": "white", "font":("Arial", 15)}
        formating_position = { "padx":40, "pady" :10, "sticky" :"nesw"}

        self.get_todays_date()
        police_names = self.get_police_names()

        #START DATE LABELS AND OPTION MENUS
        
        global month_option
        global year_option
        global police_option

        month_label = tk.Label(self,  text='Select a Month:', **formating_colour)
        month_label.grid(column=0, row=1, **formating_position)

        month_option = tk.OptionMenu(self,self.var0, *months)
        month_option.grid(column=1, row=1, **formating_position)

        year_label = tk.Label(self,  text='Select a Year:',  **formating_colour)
        year_label.grid(column=0, row=2,**formating_position)

        year_option = tk.OptionMenu(self,self.var1,  *years)
        year_option.grid(column=1, row=2, **formating_position)

        police_label = tk.Label(self,  text='Select Police Force:',  **formating_colour)
        police_label.grid(column=0, row=3,**formating_position)

        police_option = tk.OptionMenu(self,self.var2, *police_names)
        police_option.grid(column=1, row=3, **formating_position)


        #GRAPH DISPLAY BUTTONS AND QUIT 
        global age_button
        global gender_button
        global ethnicity_button
        global reason_button
        global load_button
        global reset_button
        
        load_button = tk.Button(self,  text='Connect to API, load data,', command=lambda: self.load_data(),bg="sky blue" )  
        load_button.grid(column = 0, row =4, **formating_position)
        
        reset_button = tk.Button(self,  text='Reset and load new date range/police', command=lambda: self.reset_data(),bg="sky blue",state = "disable" )  
        reset_button.grid(column = 0, row =5, **formating_position)

        age_button = tk.Button(self,  text='Age Distribution of Seach', command=lambda: self.age(), state = "disable" )  
        age_button.grid(column = 1, row =4, **formating_position)

        gender_button = tk.Button(self,  text='Gender Distibution of Search', command=lambda: self.gender(), state = "disable" )  
        gender_button.grid(column = 1, row =5, **formating_position)

        ethnicity_button = tk.Button(self,  text='Ethnicity Distribution of Search', command=lambda: self.ethnicity(), state = "disable")  
        ethnicity_button.grid(column = 1, row =6, **formating_position)

        reason_button = tk.Button(self,  text='Reason for Search', command=lambda: self.reason(), state = "disable")  
        reason_button.grid(column = 1, row =7, **formating_position)

        quit = tk.Button(self, bg= "red",text = "QUIT", command = self.destroy)
        quit.grid(column = 0, row =7, **formating_position)

