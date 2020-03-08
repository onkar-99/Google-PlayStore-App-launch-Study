from tkinter import *
from tkinter import messagebox
import matplotlib.figure
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.gridspec import GridSpec
import tkinter as tk
import re
import os
import time
from PIL import ImageTk, Image
import tkinter.messagebox as tm
import csv
from sqlalchemy import create_engine
from tkinter.scrolledtext import ScrolledText
from fractions import Fraction
from math import log, floor
ri=pd.read_csv("ratinginstall.csv", parse_dates=['Last Updated'], na_values=["not available"])
ri[['Rating']]=ri[['Rating']].fillna(value=0)
ri.dropna(how='any', inplace=True)
x=ri[ri['Current Ver'] == '2018-04-27'].index
ri.drop(x,inplace=True)
ri = ri.reset_index(drop=True)
print(ri)
rev=pd.read_csv("reviews.csv", na_values=["not available"])
rev=rev.fillna({'Translated_Review':'No review','Sentiment':'Neutral','Sentiment_Polarity':0,'Sentiment_Subjectivity':0})             
#print(rev)
def adjustWindow(window):
    w = 1000
    h = 750
    ws = screen.winfo_screenwidth()
    hs = screen.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w,h,x,y))
    window.resizable(False,False)
    #window.configure(background='black')
    
def screen_display():
    global screen
    screen = Tk()
    adjustWindow(screen)
    return

def q1():
    q1_df = ri[['App','Category','Installs']]
    set(q1_df['Category'])
    q1_df['Installs'] = q1_df['Installs'].str.strip('+')
    q1_df['Installs'] = q1_df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    q1_df = q1_df.astype(convert_dict)
    temp_q1_df = q1_df.copy()
    temp_q1_df_cate = temp_q1_df.groupby('Category').sum()
    category = list(set(temp_q1_df['Category']))
    total_installs = sum(list(temp_q1_df_cate['Installs']))
    per = []
    for cat in category:
        count = temp_q1_df_cate['Installs'][cat]
        percentage = count/total_installs * 100
        per.append(percentage)
    index = np.arange(len(category))
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    ax.pie(per,labels=None,startangle=90,autopct=lambda p : '{:,.0f}'.format(p), radius=1,wedgeprops={"edgecolor":'black','linewidth': 0.5, 'antialiased': True}) 
    label = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(category, per)]
    ax.legend(label, bbox_to_anchor=(-0.3, 0.5), loc='center left', fontsize='x-small',edgecolor='black', borderpad=1.0, title="Category-Percentage of installs", shadow=True)
    ax.set_title(label="Percentage download in each category on the playstore.", loc='center', pad=None)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()

    



def q2():
    q2_df = ri[['App','Installs']]
    q2_df['Installs'] = q2_df['Installs'].str.strip('+')
    q2_df['Installs'] = q2_df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    q2_df['Installs'] = q2_df['Installs'].astype(convert_dict)
    q2_df['Installs'].head()
    q2_df.head()
    dictionary = {"10,000 to 50,000":0,"50,000 to 1,50,000":0,"1,50,000 to 5,00,000":0,"5,00,000 to  50,00,000":0,"50,00,000 +":0}
    installs = list(q2_df['Installs'])
    for i in range(len(installs)):
        if installs[i] >=10000 and installs[i] < 50000:
            dictionary["10,000 to 50,000"] += 1
        elif installs[i] >= 50000 and installs[i] < 150000:
            dictionary["50,000 to 1,50,000"] += 1
        elif installs[i] >= 150000 and installs[i]< 500000:
            dictionary["1,50,000 to 5,00,000"] += 1
        elif installs[i] >= 500000 and installs[i] < 5000000:
            dictionary["5,00,000 to  50,00,000"] += 1
        elif installs[i] >= 500000:
            dictionary["50,00,000 +"] += 1
    print(dictionary)

#Since we have the counts now we can plot the graph
    x = []
    y = []
    for key in dictionary:
        x.append(key)
        y.append(dictionary[key])
  #  print(x,y)

    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(x,y, width=0.2 ,color=['blue', 'orange', 'green', 'red', 'violet']) 
    ax.set_ylim(bottom=10, top=3000, auto=False)
    ax.plot(x, label='Between 10,000 and 50,000')
    ax.plot(x, label='Between 50,000 and 150000')
    ax.plot(x, label=' Between 150000 and 500000')
    ax.plot(x, label='Between 500000 and 5000000')
    ax.plot(x, label='More than 5000000')
    label = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, y)]
    print(label)
    ax.legend(label, loc=9, fontsize='small',edgecolor='black', borderpad=1.0, title="Category-Percentage of installs", shadow=True)
    ax.set_ylabel('No. of Apps')
    ax.set_xlabel('Installs')
    ax.set_title(label="Apps that have managed to get downloads .", loc='center', pad=None)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()




def q3():
    q3_df = ri[['App','Category','Installs']]
    q3_df['Installs'] = q3_df['Installs'].str.strip('+')
    q3_df['Installs'] = q3_df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    q3_df['Installs'] = q3_df['Installs'].astype(convert_dict)
    q3_df_cate = q3_df.groupby('Category', as_index=False).sum()    
    category=[]
    installs = list(q3_df_cate['Installs'])
    category = q3_df.Category.unique()  
    most=max(installs)
    least=min(installs)
    most_cat=installs.index(most)
    least_cat=installs.index(least)
    l_cat=category[least_cat]
    m_cat=category[most_cat]
    print(l_cat,m_cat)
    avg=[]
    final_avg=[]
    final_cat=[]
    l=0
    q3_df_avg=q3_df.groupby('Category').mean()
    avg=list(q3_df_avg['Installs'])
    for i in range(len(avg)):
        if(avg[i] >= 250000):
            final_avg.append(int(avg[i]))
            final_cat.append(category[i])
    fig1 = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    gs = fig1.add_gridspec(ncols=4, nrows=1)
   # ax1.set_subplotspec(gs[0:2])
    #ax1 = fig1.add_subplot(gs[0, 0])
    ax = fig1.add_subplot(gs[0, 1:])    
    #ax1.bar(l_cat,l_val) 
    #  print(l_cat,l_val)
    ax.barh(final_cat,final_avg) 
    #ax1.set_xticklabels(l_cat,fontsize=7)
    ax.set_xticklabels(final_avg,fontsize=6)
    #ax1.set_ylim(bottom=14973161, top=39086024415) 
    #ax1.set_title(label="Most And list download.", loc='center', pad=None)
    ax.set_title(label="Apps having average of 2,50,000 downloads atleast.", loc='center', pad=None)
    #ax1.set_xlabel('App')
    #ax1.set_ylabel('Installs')
    ax.set_xlabel('Installs')
    ax.set_ylabel('Apps')
    ax.text(0.5,0.5,'Maximum installs is receied by Category: {}\nMinimum installs is received by Category: {}'.format(m_cat,l_cat),horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig1, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()

def q4():
    q4_df = ri[['Category','Rating']]
    q4_df_avg=q4_df.groupby('Category', as_index=False).mean()
    rat=list(q4_df_avg.Rating)
    cat = list(q4_df.Category.unique())
    large=max(rat)
    loc=rat.index(large)
    cat_final=cat[loc]
    large = round(large, 1)
    data=pd.DataFrame({'Category': cat_final,'Ratings':large}, index=[0])
    print(data)
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(q4_df_avg['Category'],q4_df_avg['Rating'])
    ax.set_title(label="Category of apps-highest maximum average ratings.", loc='center', pad=None)
    ax.set_xlabel('Category')
    ax.set_ylabel('Ratings')
    ax.set_xticklabels(q4_df_avg['Category'],rotation=90, fontsize=6)
    ax.text(0.7,0.9,'Category of app that have managed to get the highest \nmaximum average ratings from the users.: {}'.format(cat_final),horizontalalignment='right',verticalalignment='center', transform=ax.transAxes)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    def func():
        dbs= Tk()
        adjustWindow(dbs)
        dbs.configure(background='lightgrey')
        Label(dbs, text="Successfully inserted into database", font=("Open Sans", 20, 'bold'), fg='white', bg='#174873', anchor=W).place(x=335, y=0)                                         
        Label(dbs, text="Inserted data is:\n",font=("Calibri",15,"bold"), fg='white', bg='#174873').place(x=345, y=120)
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",pw="",db="python"))
        data.to_sql('quest4', con = engine, if_exists = 'replace')
        with engine.connect() as con:
            rs = con.execute('SELECT * FROM quest4')
            ind = Label(dbs, text="Index", width=5, fg='white', bg='#174873',font=("Calibri",11))
            ind.place(x=350, y=200)
            cat = Label(dbs, text="Category", width=10, fg='white', bg='#174873',font=("Calibri",11))
            cat.place(x=390, y=200)
            year = Label(dbs, text="Ratings", width=10, fg='white', bg='#174873',font=("Calibri",11))
            year.place(x=460, y=200)
            for index,row in enumerate(rs):
                Label(dbs, text=row[0], fg='white', bg='#174873',font=("Calibri",11)).place(x=350, y=220)
                Label(dbs, text=row[1], fg='white', bg='#174873',font=("Calibri",11)).place(x=390, y=220)
                Label(dbs, text=row[2], fg='white', bg='#174873',font=("Calibri",11)).place(x=480, y=220)
        dbs.mainloop()
    Button(window, text="Add to Database",width="15", bg='purple', font=("Open Sans", 12, 'bold'), fg='white',command=func).place(x=825,y=650)
    window.mainloop()
    

    
def q5():
    size=[]
    installs=[]
    q5_df = ri[['App','Installs','Size']]
    q5_df['Installs'] = q5_df['Installs'].str.strip('+')
    q5_df['Installs'] = q5_df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    q5_df['Installs'] = q5_df['Installs'].astype(convert_dict)
    size=list(q5_df['Size'])
    installs=list(q5_df['Installs'])
    #print(size[55:60])
    r = re.compile('^\d*\.?\d*k$')
    for n,i in enumerate(size):
        if r.match(i):
            i=i.strip('k')
            i=float(i)/1000
            size[n]=i
        elif (i == 'Varies with device'):
            continue
        else:
            i=i.strip('M')
            size[n]=i
    #print(size[51:61])           
    dictionary = {"Size between 10 and 20 mb":0,"Size between 20 and 30 mb":0,"More than 30 mb":0,"Varies with device":0}
    for n,i in enumerate(size):
        if i == "Varies with device":
            dictionary["Varies with device"] = dictionary["Varies with device"] + installs[n]
        else:
            if float(i) >=10 and float(i) < 20:
                dictionary["Size between 10 and 20 mb"] = dictionary["Size between 10 and 20 mb"] + installs[n] 
            elif float(i) >= 20 and float(i) < 30:
                dictionary["Size between 20 and 30 mb"] = dictionary["Size between 20 and 30 mb"] + installs[n]
            elif float(i) >= 30 :
                dictionary["More than 30 mb"] = dictionary["More than 30 mb"] + installs[n] 
        #else:
         #   dictionary["Varies with device"] = dictionary["Varies with device"] + installs[n]
    #print(dictionary)
#Since we have the counts now we can plot the graph
    x = []
    y = []
    y_f=[]
    for key in dictionary:
        x.append(key)
        y.append(dictionary[key])
#def human_format(number):
    units = ['', 'Thousand', 'Million', 'Billion', 'Trillion', 'Quadrillion']
    i=''
    for number in y:
        k = 1000.0
        magnitude = int(floor(log(number, k)))
        div=number / k**magnitude
        div = str(round(div, 2))
        i=div + ' ' + units[magnitude]
        y_f.append(i)
        #return '%.2f%s' % (number / k**magnitude, units[magnitude])
    #    p = inflect.engine()
    #    i=p.number_to_words(i)
    #    y_f.append(i)
    print(y_f)
    i=0
    lbl=''
    label = ["Size between 10 and 20 mb","Size between 20 and 30 mb","More than 30 mb","Varies with device"]
    for ind_l,l in enumerate(label):
       lbl= lbl + l + ": " + y_f[i] + '\n'
       i=i+1
    label=[lbl]
    print(label)
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(x,y) 
    #res= ['{0}: {1} '.format(i,j) for i,j in zip(label, y_f)]
    ax.legend(label, loc='upper center', fontsize='large',edgecolor='black', borderpad=1.0, shadow=True, handlelength=0)
    ax.set_ylim(bottom=3507347240, top=122568200023)    
    ax.set_title(label="No. of installs with App Size.", loc='center', pad=None)
    canvas = FigureCanvasTkAgg(fig, master=window)
    ax.set_ylabel('Installs')
    ax.set_xlabel('size')
    window= Tk()
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()
    
def q6():
    q6_df = ri[['Category','Installs','Last Updated']] 
    y_16_cat=[]
    y_17=[]
    y_18=[]
    cat=[]
    q6_df['Installs'] = q6_df['Installs'].str.strip('+')
    q6_df['Installs'] = q6_df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    q6_df['Installs'] = q6_df['Installs'].astype(convert_dict)
    q6_df['Last Updated'] = pd.DatetimeIndex(q6_df['Last Updated']).year
    temp_df_16 = q6_df.ix[(q6_df['Last Updated'] == 2016) , ['Category','Installs']]
    temp_df_17 = q6_df.ix[(q6_df['Last Updated'] == 2017) , ['Category','Installs']]
    temp_df_18 = q6_df.ix[(q6_df['Last Updated'] == 2018) , ['Category','Installs']]
    temp_df_16=temp_df_16.groupby(['Category'], as_index=False).sum()
    temp_df_17=temp_df_17.groupby(['Category'], as_index=False).sum()
    temp_df_18=temp_df_18.groupby(['Category'], as_index=False).sum()
      #print(temp_df_16)
    m16_val=max(temp_df_16.Installs)
    l16_val=min(temp_df_16.Installs)
    m16_cat=str(temp_df_16[temp_df_16['Installs']==m16_val]['Category'].item())
    l16_cat=str(temp_df_16[temp_df_16['Installs']==l16_val]['Category'].item())
    m17_val=max(temp_df_17.Installs)
    l17_val=min(temp_df_17.Installs)
    m17_cat=str(temp_df_17[temp_df_17['Installs']==m17_val]['Category'].item())
    l17_cat=str(temp_df_17[temp_df_17['Installs']==l17_val]['Category'].item())
    m18_val=max(temp_df_18.Installs)
    l18_val=min(temp_df_18.Installs)
    m18_cat=str(temp_df_18[temp_df_18['Installs']==m18_val]['Category'].item())
    l18_cat=str(temp_df_18[temp_df_18['Installs']==l18_val]['Category'].item())
    y16_cat=[m16_cat,l16_cat]
    y17_cat=[m17_cat,l17_cat]
    y18_cat=[m18_cat,l18_cat]
    y16_val=[m16_val,l16_val]
    y17_val=[m17_val,l17_val]
    y18_val=[m18_val,l18_val]
    fig = matplotlib.figure.Figure(figsize=(8,8), dpi=100, facecolor='yellow')
    gs = fig.add_gridspec(ncols=3, nrows=1)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax1.bar(y16_cat,y16_val, log=True) 
    ax2.bar(y17_cat,y17_val, log=True) 
    ax3.bar(y18_cat,y18_val, log=True)
    ax1.set_xticklabels(y16_cat,fontsize=7)
    ax2.set_xticklabels(y17_cat,fontsize=7)
    ax3.set_xticklabels(y18_cat,fontsize=7)
    ax1.set_ylim(bottom=1000, top=36052192901)
    ax2.set_ylim(bottom=1000, top=36052192901)
    ax3.set_ylim(bottom=1000, top=36052192901)
    ax1.set_xlabel('2016')
    ax2.set_xlabel('2017')
    ax3.set_xlabel('2018')
    ax1.set_ylabel('Installs')
    ax2.set_title(label="Maximum and minimum downloads for year 2016,2017,2018", loc='center', pad=None)
    ax1.text(0,0.8,'Most: {}\nLeast: {}'.format(m16_cat,l16_cat),horizontalalignment='left',verticalalignment='center', transform=ax.transAxes)
    ax2.text(0.27,0.9,'Most: {}\nLeast: {}'.format(m17_cat,l17_cat),horizontalalignment='left',verticalalignment='center', transform=ax.transAxes)
    ax3.text(0.67,0.6,'Most: {}\nLeast: {}'.format(m18_cat,l18_cat),horizontalalignment='left',verticalalignment='center', transform=ax.transAxes)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()

def q7():
    df = ri[['Installs','Android Ver']]
    labels=[]
    df['Installs'] = df['Installs'].str.strip('+')
    df['Installs'] = df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    df['Installs'] = df['Installs'].astype(convert_dict)
    df=df.groupby(['Android Ver'], as_index=False).sum()
    print(df)
    tot=0
    fin=[]
    for i, row in df.iterrows():
        if row['Android Ver'] != 'Varies with device':
            tot=tot+row['Installs']
        else:
            aver=row['Installs']
    fin=[tot,aver]
    print(fin)
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    labels=['Non Varing with device','Varies with device']
    ax.pie(fin,labels=labels,autopct='%1.1f%%',startangle=90, radius=1,wedgeprops={"edgecolor":'black','linewidth': 0.5, 'antialiased': True}) 
    label = ['{0} - {1:1.2f} '.format(i,j) for i,j in zip(labels, fin)]
    ax.legend(label, loc='left upper', fontsize='x-small',edgecolor='black', borderpad=1.0, title="Category-Percentage of installs", shadow=True)
    ax.set_title(label="Percentage download for apps having android version as 'Varies with Device'.", loc='center', pad=None)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()
def q8():
    df = ri[['Category','Installs','Last Updated']]
    print(df)
    df['Installs'] = df['Installs'].str.strip('+')
    df['Installs'] = df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    df['Installs'] = df['Installs'].astype(convert_dict)
    df['Last Updated'] = pd.DatetimeIndex(df['Last Updated']).year
    print(df)
    df_main=df[(df['Category'] == 'SPORTS') | (df['Category'] == 'ENTERTAINMENT') | (df['Category'] == 'SOCIAL') | (df['Category'] == 'NEWS_AND_MAGAZINES') | (df['Category'] == 'EVENTS') | (df['Category'] == 'TRAVEL_AND_LOCAL') | (df['Category'] == 'GAME')]
    print(df_main)
    df_main.drop_duplicates(subset=['Category','Installs','Last Updated'],keep='first', inplace=True)
    df_main = df_main.groupby(['Category','Last Updated'], as_index=False).sum()
    print(df_main)
    df_sports=df[df['Category'] == 'SPORTS'].copy()    
    df_sports.drop_duplicates(subset=['Installs','Last Updated'],keep='first', inplace=True)
    df_sports = df_sports.groupby('Last Updated', as_index=False).sum()
    df_ent=df[df['Category'] == 'ENTERTAINMENT'].copy()    
    df_ent.drop_duplicates(subset=['Installs','Last Updated'],keep='first', inplace=True)
    df_ent = df_ent.groupby('Last Updated', as_index=False).sum()
    df_social=df[df['Category'] == 'SOCIAL'].copy()    
    df_social.drop_duplicates(subset=['Installs','Last Updated'],keep='first', inplace=True)
    df_social = df_social.groupby('Last Updated', as_index=False).sum()
    df_news=df[df['Category'] == 'NEWS_AND_MAGAZINES'].copy()    
    df_news.drop_duplicates(subset=['Installs','Last Updated'],keep='first', inplace=True)
    df_news = df_news.groupby('Last Updated', as_index=False).sum()
    df_event=df[df['Category'] == 'EVENTS'].copy()    
    df_event.drop_duplicates(subset=['Installs','Last Updated'],keep='first', inplace=True)
    df_event = df_event.groupby('Last Updated', as_index=False).sum()
    df_travel=df[df['Category'] == 'TRAVEL_AND_LOCAL'].copy()    
    df_travel.drop_duplicates(subset=['Installs','Last Updated'],keep='first', inplace=True)
    df_travel = df_travel.groupby('Last Updated', as_index=False).sum()
    df_game=df[df['Category'] == 'GAME'].copy()    
    df_game.drop_duplicates(subset=['Installs','Last Updated'],keep='first', inplace=True)
    df_game = df_game.groupby('Last Updated', as_index=False).sum()
    #print(df_social)
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax1 = fig.add_subplot(331)
    ax2 = fig.add_subplot(332)
    ax3 = fig.add_subplot(333)
    ax4 = fig.add_subplot(334)
    ax5 = fig.add_subplot(335)
    ax6 = fig.add_subplot(336)
    ax7 = fig.add_subplot(337)
    ax8 = fig.add_subplot(338)
    ax1.plot(df_sports['Last Updated'],df_sports['Installs'], '-o', color='y', label='Sports')
    ax2.plot(df_ent['Last Updated'],df_ent['Installs'], '-o', color='b',label='Entertainment')
    ax3.plot(df_social['Last Updated'],df_social['Installs'], '-o', color='#FFA500',label='Social')
    ax4.plot(df_news['Last Updated'],df_news['Installs'], '-o', color='g',label='News')
    ax5.plot(df_event['Last Updated'],df_event['Installs'], '-o', color='purple',label='Event')
    ax6.plot(df_travel['Last Updated'],df_travel['Installs'], '-o', color='grey',label='Travel')
    ax7.plot(df_game['Last Updated'],df_game['Installs'], '-o', color='r',label='Game')
    ax8.plot(df_sports['Last Updated'],df_sports['Installs'], '-o', color='y', label='Sports')
    ax8.plot(df_ent['Last Updated'],df_ent['Installs'], '-o', color='b',label='Entertainment')
    ax8.plot(df_social['Last Updated'],df_social['Installs'], '-o', color='#FFA500',label='Social')
    ax8.plot(df_news['Last Updated'],df_news['Installs'], '-o', color='g',label='News')
    ax8.plot(df_event['Last Updated'],df_event['Installs'], '-o', color='purple',label='Event')
    ax8.plot(df_travel['Last Updated'],df_travel['Installs'], '-o', color='grey',label='Travel')
    ax8.plot(df_game['Last Updated'],df_game['Installs'], '-o', color='r',label='Game')
    #ax.set_xticklabels(labels=" ")
    #ax.set_ylim(bottom=0, top=-100)
    ax8.legend(bbox_to_anchor=[0.5,0.5],edgecolor='black', borderpad=1.0, title="Installs for each year", shadow=True)
    #ax.set_xlabel('Apps')
    #ax.set_ylabel('Percentage installs of each app (%)')
    #ax.set_title('Percentage increase or decrease in the downloads')
    ax1.text(1,1.3,'Most likely to be downloaded in coming years: GAME\nas the installs for Game has increased over the years, ',horizontalalignment='left',verticalalignment='center', transform=ax1.transAxes)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    plt.tight_layout()
    def func():
        dbs= Tk()
        Label(dbs, text="Successfully inserted into database", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=345, y=200)                                         
        Label(dbs, text="Inserted data is:\n",font=("Calibri",20,"bold"), bg='blue', fg='orange').place(x=345, y=120)
        engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root",pw="",db="python"))
        df_main.to_sql('quest8', con = engine, if_exists = 'append')
        with engine.connect() as con:
            rs = con.execute('SELECT * FROM quest8')
            ind = Label(dbs, text="Index", width=5)
            ind.grid(row=0, column=0)
            cat = Label(dbs, text="Category", width=10)
            cat.grid(row=0, column=1)
            year = Label(dbs, text="Year", width=10)
            year.grid(row=0, column=2)
            inst = Label(dbs, text="Installs", width=10)
            inst.grid(row=0, column=3)
            for index,row in enumerate(rs):
                Label(dbs, text=row[0]).grid(row=index+1, column=0)
                Label(dbs, text=row[1]).grid(row=index+1, column=1)
                Label(dbs, text=row[2]).grid(row=index+1, column=2)
                Label(dbs, text=row[3]).grid(row=index+1, column=3)
        dbs.mainloop()
    Button(window, text="Add to Database",width="15", bg='purple', font=("Open Sans", 12, 'bold'), fg='white',command=func).place(x=825,y=650)
    window.mainloop()  
    
def q9():
    df = ri[['App','Installs','Rating']]
    df['Installs'] = df['Installs'].str.strip('+')
    df['Installs'] = df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    df['Installs'] = df['Installs'].astype(convert_dict)
    df=df[df['Installs']>=100000].copy()
    A=df[df['Rating']>=4.1].copy()
    B=df[df['Rating']<4.1].copy()
    #print(B)
    A.drop_duplicates(subset=['Rating','Installs'],keep='first', inplace=True)
    B.drop_duplicates(subset=['Rating','Installs'],keep='first', inplace=True)
    a_rat=[]
    b_rat=[]
    a_inst=[]
    b_inst=[]
    a_rat=list(A['Rating'])
    b_rat=list(B['Rating'])
    a_inst=list(A['Installs'])
    b_inst=list(B['Installs'])
    #print(a_inst,b_inst)
    la=len(a_rat)
    lb=len(b_rat)
    cor=df['Installs'].corr(df['Rating'])
    cor=round(cor, 3)
    print(cor)
    #labels=df.Installs.unique()
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    ax.scatter(a_rat,a_inst, label='Rating >= 4.1') 
    ax.scatter(b_rat,b_inst,label='Rating < 4.1') 
    ax.legend(edgecolor='black', borderpad=1.0, title="Rating values", shadow=True)
    #ax.set_xticklabels(labels)
    #ax.set_ylim(10000,max(a_inst))
    #ax.set_ylim(bottom=50000, top=1500000000)
    ax.set_xlabel('Rating', fontsize=13)
    ax.set_ylabel('Installs', fontsize=13)
    ax.set_title('No Of Installs According To Rating',fontsize=24)
    ax.text(0.3,0.9,'Total apps where rating >= 4.1 is {}\nTotal apps where rating < 4.1 is {}\n\nThus we can say all the apps that have\n downloads > 1,00,000 have not managed to get rating >=4.1'.format(la,lb),horizontalalignment='left',verticalalignment='center', transform=ax.transAxes)
    ax.text(0.1,0.5,'The correlation between ratings received and no of downloads is {}\nThus there is negative correlation as value is closer to 0'.format(cor),horizontalalignment='left',verticalalignment='center', transform=ax.transAxes)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()
    

    
def q10():
    global screen2,appName
    cols={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December',}
    cat_new=[]
    month=[]
    key=[]
    value=[]
    df = ri[['App','Category','Installs','Last Updated','Content Rating']] 
    df['Installs'] = df['Installs'].str.strip('+')
    df['Installs'] = df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    df['Installs'] = df['Installs'].astype(convert_dict)
    df['Last Updated'] = pd.DatetimeIndex(df['Last Updated']).month           
    #print(df.columns)
    idx=df.groupby(['Category'])['Installs'].transform(max) == df['Installs']
    q10_df=df.loc[idx]
    #print(q10_df[['Category','Installs','Last Updated']])
    q10_df.drop_duplicates(subset=['Category','Installs','Last Updated'],keep='first', inplace=True)
    q10_df=q10_df.sort_values(['Category'])
    q10_df = q10_df.reset_index(drop=True)
    #print(q10_df[['Category','Last Updated']])
    cat=list(q10_df['Category'])
    inst=list(q10_df['Installs'])
    mon=list(q10_df['Last Updated'])
    #print(cat_new,len(cat_new))
    #print(month)
    #SCATTER
    #print(cols)
    df_teen = df.ix[(df['Content Rating'] == 'Teen') , ['App','Installs']]
    df_mature = df.ix[(df['Content Rating'] == 'Mature 17+') , ['App','Installs']]
    sum_teen = df_teen['Installs'].sum()
    sum_mature = df_mature['Installs'].sum()
    ratio=[]
    ratio= [sum_teen,sum_mature]
    app_teen=list(df_teen['App'])
    app_mature=list(df_mature['App'])
    #print(df_teen)
    labels=['Apps qualified as Teen','Apps qualified as Mature 17+']
    cate=[]
    cate=df['Category'].unique()
    #print(cate)
    screen2=Tk()
    adjustWindow(screen2)
    appName=StringVar(screen2)
    droplist = OptionMenu(screen2, appName, *cate)
    droplist.config(width=80)
    appName.set('--Choose Your Category--')
    droplist.place(x=25, y=80)
    def func():
        global screen2,appName
        df_val=q10_df[q10_df['Category'] == appName.get()]
        #print(df_val[['Category','Last Updated']])
        cat=list(df_val['Category'])
        inst=list(df_val['Installs'])
        #print(inst)
        mon=list(df_val['Last Updated'])
        #print(mon)
        for j,item in enumerate(cat):
        #matches = -1
            month.append([])
            for i,x in enumerate(cat):
                if (item == x) and (x not in cat_new):
                
                    month[j].append(mon[i])
        #if matches >= 1: 
            if item not in cat_new:
                cat_new.append(item)
            while month.count([]) > 0:
                month.remove([])
        #print(month)
        #print(cat_new)
    #print(cat_new,len(cat_new))
    #print(month)
    #SCATTER
    #print(cols)
        df_teen = df.ix[(df['Content Rating'] == 'Teen') , ['App','Installs']]
        df_mature = df.ix[(df['Content Rating'] == 'Mature 17+') , ['App','Installs']]
        sum_teen = df_teen['Installs'].sum()
        sum_mature = df_mature['Installs'].sum()
        ratio=[]
        ratio= [sum_teen,sum_mature]
        app_teen=list(df_teen['App'])
        app_mature=list(df_mature['App'])
    #print(df_teen)
        labels=['Apps qualified as Teen','Apps qualified as Mature 17+']
    #    screen2.mainloop()
        fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
        #ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(111)
        s=""
        y=""
        for xe, ye in zip(cat_new, month):
            for i in ye:
            #print(xe,ye)
                y=cols[i]
                s=s+","+y
        ax2.text(-0.1,0.8,'Month(s) which has received maximum download\nfor {} category is/are {}'.format(appName.get(),s),horizontalalignment='left',verticalalignment='center', transform=ax.transAxes)
            
        #ax1.scatter([xe] * len(ye), ye, color='b')
    #ax.scatter(cat,mon) 
        #ax1.scatter(cat_new,month)
        #ax1.set_xticklabels(cat_new,fontsize=7)
        #ax1.set_yticklabels(cols.values(),fontsize=7)
        #ax1.set_yticks([1,2,3,4,5,6,7,8,9,10,11,12])
        #ax1.set_xticks(np.arange(len(cat_new)))
        frac=Fraction(sum_teen,sum_mature)
        ax2.pie(ratio,labels=labels,startangle=90,autopct='%.2f%%', radius=0.7,wedgeprops={"edgecolor":'black','linewidth': 0.5, 'antialiased': True})
        ax2.legend(bbox_to_anchor=(1, 0))
        ax2.set_title('Ratio of apps qualified as Teen vs Mature 17+')
        #ax2.set_title('Month which received maximum download for each category')
        ax2.text(0.5,0.9,'             {}\nRatio is  -------------------     =   {}\n             {}'.format(sum_teen,frac,sum_mature),horizontalalignment='left',verticalalignment='center', transform=ax.transAxes)
        #window= Tk()
        canvas = FigureCanvasTkAgg(fig, master=screen2)
        canvas.get_tk_widget().pack()
        canvas.draw()
        #screen2.mainloop()
    Button(screen2, text="CONFIRM",width="8", bg='purple', font=("Open Sans", 12, 'bold'), fg='white',command=func).place(x=900,y=670)
    screen2.mainloop()
    
def q11():
    q1=[]
    q2=[]
    q3=[]
    q4=[]
    q1_val=[]
    q2_val=[]
    q3_val=[]
    q4_val=[]
    df = ri[['App','Installs','Last Updated']]
    df['Installs'] = df['Installs'].str.strip('+')
    df['Installs'] = df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    df['Installs'] = df['Installs'].astype(convert_dict)
    df['Last Updated'] = pd.to_datetime(df['Last Updated'])
    #print(df.head())
    df_quat=df.resample('Q', convention='start', on='Last Updated',label='left').agg('sum')
    df_quat['Last Updated'] = df_quat.index.values
    #print(df_quat)
    #print(df_quat.dtypes)
    for i in range (len(df_quat['Last Updated'])):
        if i%4==0:
            q1.append(str(df_quat['Last Updated'][i].year))
            q1_val.append(df_quat['Installs'][i])
        if i%4==1:
            q2.append(str(df_quat['Last Updated'][i].year))
            q2_val.append(df_quat['Installs'][i])
        if i%4==2:
            q3.append(str(df_quat['Last Updated'][i].year))
            q3_val.append(df_quat['Installs'][i])
        if i%4==3:
            q4.append(str(df_quat['Last Updated'][i].year))
            q4_val.append(df_quat['Installs'][i])
    labels=[2010,2011,2012,2013,2014,2015,2016,2017,2018]
    q3.append(2018)
    q4.append(2018)
    q3_val.append(0.0)
    q4_val.append(0.0)
    x = np.arange(len(q1_val))
    y=np.arange(len(q3_val))
    width=0.5
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(x,q1_val, width, label='Quarter-1(Jan-Mar)', log=True,edgecolor='black')
    ax.bar(x,q2_val, width,color='r', bottom=q1_val, label='Quarter-2(Apr-Jun)', log=True,edgecolor='black')
    ax.bar(x,q3_val, width,color='#0100b3', bottom=np.add(q1_val,q2_val), label='Quarter-3(Jul-Sept)', log=True,edgecolor='black')
    ax.bar(x,q4_val, width,color='y', bottom=np.add(q2_val,q3_val), label='Quarter-4(Oct-Dec)', log=True,edgecolor='black')
    ax.set_ylim(bottom= 1000, top= 272227910688)
    ax.set_xticks(x)
    ax.set_xticklabels(labels,fontsize=7)
    ax.set_xlabel('Years')
    ax.set_ylabel('Installs')
    ax.legend(edgecolor='black', borderpad=1.0, title="Different quarters of year", shadow=True)
    ax.set_title(label="Highest number of install for each app .", loc='center', pad=None)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()

def q12():
    app=[]
    pos=[]
    neg=[]
    approx=[]
    approx_app=[]
    pos_cat=[]
    neg_cat=[]
    df = rev[['App','Sentiment']]
    #df_count = df.assign(Positive = lambda x: [1 if row.Sentiment == 'Positive' else 0 for index, row in x.iterrows()],Negative = lambda x: [1 if row.Sentiment == 'Negative' else 0 for index, row in x.iterrows()])
    df_count= pd.get_dummies(df, columns=['Sentiment'])
    df_count.rename(columns={'Sentiment_Positive':'Positive','Sentiment_Negative':'Negative','Sentiment_Neutral':'Neutral'},inplace=True)
    #print(df_count)
    df_count = df_count.groupby('App').agg({"Positive":sum, "Negative":sum}).reset_index()
    #print(df.head())
    app=list(df_count['App'])
    pos=max(df_count['Positive'])
    pos_cat=str(df_count[df_count['Positive']==pos]['App'].item())
    #print(pos,pos_cat)
    neg=max(df_count['Negative'])
    neg_cat=str(df_count[df_count['Negative']==neg]['App'].item())
    cat=[pos_cat, neg_cat]
    val=[pos,neg]
    df_count['Div'] = df_count['Positive'] / df_count['Negative']
    print(df_count)
    for i, row in df_count.iterrows():
        if (row['Div'] >= 0.9 and row['Div'] <= 1.1):
            approx.append(row['Div'])
            approx_app.append(row['App'])
    
    print(approx,approx_app)
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.bar(pos_cat,pos,color='r', label= 'Positive Sentiments')
    ax1.bar(neg_cat,neg,color='g',label= 'Negative Sentiments')
    
 #   (markerline, stemlines, baseline) = ax2.stem(approx_app,approx)
    #ax2.setp(baseline, visible=False)
    ax2.plot(approx_app,approx)
    ax1.legend(loc='upper right',edgecolor='black', borderpad=1.0, title=" Maximum Sentiments", shadow=True)
    ax2.set_xticklabels(approx_app,rotation=90,fontsize=7)
    #ax.set_yticklabels(cat,fontsize=7)
    ax1.set_title(label="Most positive and negative sentiments.", loc='center', pad=None)
    ax2.set_title(label="Apps having positive-negative\n sentiment ratio between 0.9 and 1", loc='center', pad=None)
    ax1.set_ylabel('Sentiments')
    ax1.set_xlabel('Apps')
    ax2.set_xlabel('Apps')
    ax2.set_ylabel('Sentiments')
    #ax1.text(0.2,1,'sentiment analysis positive and negative:\n {} {}'.format(pos_cat,neg_cat),horizontalalignment='center',verticalalignment='center', transform=ax1.transAxes)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()

def q13():
    df = rev[['App','Sentiment_Polarity','Sentiment_Subjectivity']]
    sp = list(df['Sentiment_Polarity'])
    s_sub = list(df['Sentiment_Subjectivity'])
    s_sub4=list(df[df['Sentiment_Polarity'] == 0.4]['Sentiment_Subjectivity'].copy())
    cor=df['Sentiment_Polarity'].corr(df['Sentiment_Subjectivity'])
    cor=round(cor, 3)
    print(cor)
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    y=[0.4]
    ax2.plot(s_sub4, c='r', label='Sentiment subjectivity for sentiment polarity of 0.4',zorder=1)
    ax1.scatter(s_sub,sp, label='Sentiment subjectivity and its respective sentiment polariity',zorder=2)
    ax1.set_xlabel('Sentiment Subjectivity', fontsize=10)
    ax1.set_ylabel('Sentiment Polarity', fontsize=10)
    ax2.set_xlabel('Sentiment Subjectivity', fontsize=10)
    ax2.set_ylabel('Sentiment Polarity', fontsize=10)
    #ax1.set_title('Relation between Sentiment Subjectivity\n and Sentiment Polarity',fontsize=18)
    #ax1.legend(loc='upper left',edgecolor='black', borderpad=1.0, title="Rating values", shadow=True)
    ax2.legend(loc='upper right',edgecolor='black', borderpad=1.0, title="Rating values", shadow=True)
    ax1.text(0.1,1.05,'The correlation between sentiment polarity\n and sentiment subjectivity is {}\nThus there is inverse relation between them.'.format(cor),horizontalalignment='left',verticalalignment='center', transform=ax1.transAxes)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()
def q15():
    df = rev[['App','Sentiment']]
    d={}
    y=[]
    x=['Positive','Neutral','Negative']
    colors=['r','b','g']
    df=df[df['App'] == '10 Best Foods for You']
    #print(df)
    #df_count = df.groupby('App', as_index=False)['Sentiment'].agg({"Positive":count, "Negative":sum, "Neutral":sum})
    df_count=df['Sentiment'].value_counts().reset_index()
    y=df_count['Sentiment'].tolist()
    #x=df_count.index.tolist()
    print(y)
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    ax.bar(x,y, color=colors, width=0.5)
    #ax.set_xticklabels(['Positive','Neutral','Negative'])
    ax.set_xlabel('Sentiments', fontsize=10)
    ax.set_ylabel('Count', fontsize=10)
    ax.set_title('Analysis on "10 Best Foods for You"',fontsize=18)
    ax.text(0.3,0.5,'Yes, it is advisable to launch such apps as they have received\nmore no of positive sentiments as compare to negative sentiments',horizontalalignment='left',verticalalignment='center', transform=ax.transAxes)
    #label = ['Positive-168','Neutral-28','Negative-10']
    #ax.legend(label,loc='upper right',edgecolor='black', borderpad=1.0, title="Rating values", shadow=True)
    #ax.set_ylim(bottom=0, top=200)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()
def q16():
    global window,yrName,df,q16_df
    cols={1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October',11:'November',12:'December',}
    df = ri[['Installs','Last Updated']]
    df['Installs'] = df['Installs'].str.strip('+')
    df['Installs'] = df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    df['Installs'] = df['Installs'].astype(convert_dict)
    df['Year'] = pd.DatetimeIndex(df['Last Updated']).year
    df['Month'] = pd.DatetimeIndex(df['Last Updated']).month
    df.drop(columns='Last Updated',inplace=True)
    #print(df)
    def graphh():
        global yrName,df,q16_df
        d = ['Sum1','Average']
        year=int(yrName.get())
        print(year)
        temp_df = df[df['Year'] == year]
        temp_df = temp_df.reset_index(drop=True)
        temp_df.drop(columns='Year',inplace=True)
        print(temp_df)
        mean=int(temp_df['Installs'].mean())
        print(mean)
        temp_df=temp_df.groupby("Month",as_index=False)['Installs'].agg('sum')
        print(temp_df)
        mean=int(temp_df['Installs'].mean())
        def closest(lst, K): 
            return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]
        ans=closest(list(temp_df['Installs']),mean)
        ans=int(temp_df[temp_df['Installs'] == ans]['Month'])
        ans=cols[ans]
        print(ans)
        fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
        ax= fig.add_subplot(111)
        ax.bar(temp_df['Month'],temp_df['Installs'])
        ax.axhline(y=mean, color='r', linestyle='-')
        ax.set_xlabel('Months', fontsize=16)
        ax.set_ylabel('No of Downloads', fontsize=16)
        ax.set_xticklabels(cols.values(),fontsize=7)
        ax.set_xticks([1,2,3,4,5,6,7,8,9,10,11,12])
        #plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], df['Last Updated'], fontsize=10)
        ax.set_title('Analysis for "Month wise Downloads"',fontsize=24)
        ax.text(0.5,0.7,'Month which is best indicator for\n average installs for the year {} is {} '.format(year,ans),horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)
        graph= Toplevel(window)
        canvas = FigureCanvasTkAgg(fig, master=graph)
        canvas.get_tk_widget().pack()
        canvas.draw()
        graph.mainloop()
    window=Tk()
    adjustWindow(window)
    yr=[]
    yr=sorted(df['Year'].unique())
    yrName = StringVar(window)
    droplist = OptionMenu(window, yrName, *yr)
    droplist.config(width=80)
    yrName.set('--Choose Year--')
    droplist.place(x=25, y=80)
    Button(window, text="Confirm",width="15", bg='purple', font=("Open Sans", 12, 'bold'), fg='white',command=graphh).place(x=825,y=650)
    window.mainloop()

   
def q17():
    size=[]
    installs=[]
    q5_df = ri[['Installs','Size']]
    q5_df['Installs'] = q5_df['Installs'].str.strip('+')
    q5_df['Installs'] = q5_df['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    q5_df['Installs'] = q5_df['Installs'].astype(convert_dict)
    size=list(q5_df['Size'])
    installs=list(q5_df['Installs'])
    print(q5_df)
    r = re.compile('^\d*\.?\d*k$')
    for n,i in enumerate(size):
        if r.match(i):
            i=i.strip('k')
            i=float(i)/1000
            size[n]=float(i)
        elif (i == 'Varies with device'):
            continue
        else:
            i=i.strip('M')
            size[n]=float(i)
    #print(size)
    q5_df['Size']=size
    q5_df = q5_df[q5_df.Size != 'Varies with device']
    print(q5_df[q5_df['Size'].between(10, 20)])  
    bins = [-1, 1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels=['In kb','1-10','10-20','20-30','30-40','40-50','50-60','60-70','70-80','80-90','90-100']
    q5_df=q5_df.groupby(pd.cut(q5_df['Size'], bins=bins, labels=labels), as_index=False).mean()
    q5_df['Size']=labels
    q5_df['Installs']=q5_df['Installs'].astype(int)
    print (q5_df)         
#Since we have the counts now we can plot the graph
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(q5_df['Size'],q5_df['Installs']) 
    ax.set_title(label="No. of installs with App Size.", loc='center', pad=None)
    ax.set_ylabel('Installs')
    ax.set_xlabel('App size in between')
    ax.text(0.4,0.7,'We can see there is a positive trend with increase in app size.\nThere is a sudden increase in downloads for app size between 50-70Mb\nand decrease from 70-80Mb',horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)    
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()

def q19():
    df = ri[['Category','Reviews']]
    print(df)
    convert_dict = {'Reviews':int}
    df['Reviews'] = df['Reviews'].astype(convert_dict)
    df_avg = df.groupby('Category', as_index=False).mean()
    print(df_avg)
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(df_avg['Category'],df_avg['Reviews'])
    ax.set_xlabel('Categories', fontsize=10)
    ax.set_ylabel('Reviews', fontsize=10)
    ax.set_xticklabels(df_avg['Category'],rotation =90)
    ax.set_title('Average reviews obtained by each category',fontsize=18)
    #ax.legend(loc='upper left',edgecolor='black', borderpad=1.0, title="Rating values", shadow=True)
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()
    
def q20():
    df1 = ri[['App','Installs','Rating']]
    df2 = rev[['App','Sentiment_Polarity']]
    df1['Installs'] = df1['Installs'].str.strip('+')
    df1['Installs'] = df1['Installs'].str.replace(',','')
    convert_dict = {'Installs':int}
    df1['Installs'] = df1['Installs'].astype(convert_dict)
    df2=df2[df2['Sentiment_Polarity'].between(0.9,1,inclusive=True)]
    print(df2)
    df1=df1[df1['Rating'] == 4.5]
    print(df1)
    df=df1.merge(df2, on='App')
    print(df)
    df_sum = df.groupby('App', as_index=False)['Installs'].sum()
    print(df_sum)
    fig = matplotlib.figure.Figure(figsize=(10,10), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(df_sum['App'],df_sum['Installs'])
    ax.set_xlabel('App', fontsize=10)
    ax.set_ylabel('Installs', fontsize=10)
    ax.set_xticklabels(df_sum['App'],rotation =90)
    ax.set_title('Total sum for all those apps having rating as 4.5 and sentiment polarity between 0.9 and 1',fontsize=10)
    #ax.legend(loc='upper left',edgecolor='black', borderpad=1.0, title="Rating values", shadow=True)
    ax.legend()
    window= Tk()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack()
    canvas.draw()
    window.mainloop()
    
    
def nextpage():
    global screen
    screen = Tk()
    screen.title("Google PlayStore App launch Study")  # mentioning title of the window 
    adjustWindow(screen) 
    Label(screen, text="", bg='lightblue',width='130', height='110').place(x=45, y=50)
    Button(screen, text="9) All those apps who have managed to get over 1,00,000 downloads, have they managed to get an averagerating\n of 4.1 and above? An we conclude something in co-relation to the number of downloads and the ratings received ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q9).place(x=45,y=60)              
    Button(screen, text="10) Across all the years ,which month has seen the maximum downloads fr each of the category.\n What is the ratio of downloads for the app that qualifies as teen versus mature17+   ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q10).place(x=45,y=120)              
    Button(screen, text="11) Which quarter of which year has generated the highest number of install for each app used in the study?   ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q11).place(x=45,y=180)              
    Button(screen, text="12) Which of all the apps given have managed to generate the most positive and negative sentiments.\n Also figure out the app which has generated approximately the same ratio for positive and negative sentiments. ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q12).place(x=45,y=225)              
    Button(screen, text="13) Study and find out the relation between the Sentiment-polarity and sentimentsubjectivity of all the apps.\n What is the sentiment subjectivity for a sentiment polarity of 0.4.  ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q13).place(x=45,y=290)              
    Button(screen, text="14) Generate an interface where the client can see the reviews categorized as positive.negative and neutral,\nonce they have selected the app from a list of apps available for the study.    ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q14).place(x=45,y=350)              
    Button(screen, text="15) Is it advisable to launch an app like ’10 Best foods for you’? Do the users like these apps?    ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q15).place(x=45,y=410)              
    Button(screen, text="16) Which month(s) of the year , is the best indicator to the avarage downloads that an app earn more price", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q16).place(x=45,y=455)              
    Button(screen, text="17) Does the size of the App influence the number of installs  that it gets?\nif,yes the trend is positive or negative with the increase in the app size.", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q17).place(x=45,y=500)              
    Button(screen, text="18) Provide an interface to add new data to both the datasets provided.The data needs\nto be added to the excel sheets. ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q18).place(x=45,y=560)              
    Button(screen, text="19) Find the average reviews received by each category  ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q19).place(x=45,y=620)              
    #Button(screen, text="19) In next year which category apps to upload more so that Downloads will increase?  ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q19).place(x=45,y=620)              
    Button(screen, text="20) Find installs for all those apps who have received ratings for 4.5 and have sentiment polarity between 0.9 and 1 ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q20).place(x=45,y=660)              
    Button(screen, text="GO BACK",width="10", bg='purple', font=("Calibri", 15, 'bold'), fg='white',command=second_screen).place(x=890,y=680)

  

           

def q14():
    df = ri[['App','Category','Installs','Android Ver']]
    global window, appName,catName
    cat=[]
    app=[]
    #adjustWindow(screen2) # configuring the window
    df1 = rev[['App','Sentiment','Translated_Review']]
    df2 = ri[['App','Category']]
    #df=df[set((df1['App'])) & set((df2['App']))]
    df = pd.merge(df1, df2, how='inner', left_on='App', right_on='App')
    df.drop(df[df['Translated_Review']== 'No review'].index, inplace=True)
    #print(df)
    cat=list(df['Category'].unique())
    app=list(df['App'].unique())
    print(len(app)) 
    window=Tk()     
    def graph(app):
        global q14_df,window,appName
        screen = Tk()
        #adjustWindow(screen)
        #window.destroy()
        #print(app)
        q14_df= q14_df[q14_df['App'] == app]
        print(q14_df[['App','Sentiment','Translated_Review']])
        df_pos= q14_df[q14_df['Sentiment'] == 'Positive']
        print(df_pos[['App','Sentiment','Translated_Review','Sentiment']])
        df_neg= q14_df[q14_df['Sentiment'] == 'Negative']
        df_nut= q14_df[q14_df['Sentiment'] == 'Neutral']   
        pos=""
        neg=""
        nut=""
        for index, row in df_pos.iterrows(): 
            pos= pos + row["Translated_Review"] + "\n\n"
        for index, row in df_neg.iterrows(): 
            neg= neg + row["Translated_Review"] + "\n\n"
        for index, row in df_nut.iterrows(): 
            nut= nut + row["Translated_Review"] + "\n\n"
        spos=ScrolledText(screen,bg='#ddcb8b',relief=SUNKEN,height=10,width=100,font='TkFixedFont')
        sneg=ScrolledText(screen,bg='#ddcb8b',relief=SUNKEN,height=10,width=100,font='TkFixedFont')
        snut=ScrolledText(screen,bg='#ddcb8b',relief=SUNKEN,height=10,width=100,font='TkFixedFont')
        Label(screen, text='POSITIVE',height="1", width="8", font=("Open Sans", 20, 'bold'), bg='pink', fg='black').place(x=15, y=160)
        Label(screen, text='NEGATIVE',height="1", width="8", font=("Open Sans", 20, 'bold'), bg='pink', fg='black').place(x=15, y=360)
        Label(screen, text='NEUTRAL',height="1", width="8", font=("Open Sans", 20, 'bold'), bg='pink', fg='black').place(x=15, y=560)
        Label(screen, text="Welcome To Review Page", width='50', height="2", font=("Calibri", 30,'bold'), fg='white', bg='purple', anchor = CENTER).place(x=0, y=0)
        spos.place(x=150,y=125)
        sneg.place(x=150, y=330)
        snut.place(x=150,y=525)
        spos.insert(0.0,pos)
        sneg.insert(0.0,neg)
        snut.insert(0.0,nut)
        screen.mainloop()
    def disp(app):
        global app_val,window,appName
        app_val=app
        #b=Button(window, text="CONFIRM",width="15", bg='purple', font=("Open Sans", 12, 'bold'), fg='white',command=graph())
        #b.place(x=825,y=650)
        graph(app_val)
        
    def findcat(cat):
        global q14_df,window,appName
        cat_name=cat
        q14_df= df[df['Category'] == cat]
        #print(q7_df)
        app=q14_df['App'].unique()
        appName = StringVar(window)
        droplist = OptionMenu(window, appName, *app,command=disp)
        #, command=lambda: (app_name := appName.get()))
        droplist.config(width=80)
        appName.set('--Choose Your App--')
        droplist.place(x=275, y=80)
    
    window.title("Welcome To The Review Page")
    #adjustWindow(window)
    catName = StringVar(window)
    droplist = OptionMenu(window, catName, *cat,command=findcat)
    droplist.config(width=80)
    catName.set('--Choose Your Category--')
    droplist.place(x=25, y=80)
    #app_name=appName.get()
    #cat_name=func.cat_name
    #print(cat_name,app_name)
    window.mainloop()
    
def validate_rating(): 
    if app.get() != '':
        if category.get() != 'Choose Your Category':
            if re.match("^\d\.\d$", ratings.get()):
                if re.match("^\d*$", reviews.get()):
                    if re.match("^\d*(k|M)$", size.get()):
                        if re.match("^\d*\+$", installs.get()):
                            if ((price.get() != '$0') and (apptype.get() == 2) or ((price.get() == '$0') and (apptype.get() == 1))):
                                if re.match("^\$[0-9]+(\.[0-9][0-9])?$", price.get()):
                                    if contentrating.get() != 'Choose Content Rating':
                                        if genres.get() != 'Choose Your Genre':
                                            if re.match("^\d{1,2}\/\d{1,2}\/\d{4}$", lastupdated.get()):
                                                if re.match("^(\d\.?\d.?\d|Varies with device)$", currentver.get()):
                                                    if re.match("^(\d\.?\d.?\d and up|Varies with device)$", androidver.get()):
                                                        return True
                                                    else:
                                                        messagebox.showerror("Error", "Enter Valid Android Version")
                                                        return False
                                                else:
                                                    messagebox.showerror("Error", "Enter Valid Currrent Version")
                                                    return False
                                            else:
                                                messagebox.showerror("Error", "Enter Valid Date")
                                                return False
                                        else:
                                            messagebox.showerror("Error", "Select valid Genre")
                                            return False
                                        
                                    else:
                                        messagebox.showerror("Error", "Select valid Content Rating")
                                        return False
                                else:
                                    messagebox.showerror("Error", "Enter valid amount greater than $0")
                                    return False
                            else:
                                messagebox.showerror("Error", "Enter valid amount greater than $0")
                                return False
                        else:
                            messagebox.showerror("Error", "Enter Valid Installs")
                            return False
                    else:
                        messagebox.showerror("Error", "Enter Valid Size")
                        return False
                else:
                    messagebox.showerror("Error", "Enter Valid Reviews")
                    return False
            else:
                messagebox.showerror("Error", "Enter Valid Ratings")
                return False
        else:
            messagebox.showerror("Error", "Choose valid Category")
            return False
    else:
        messagebox.showerror("Error", "Please enter valid Application Name")
        return False


  
def check_entry():
    global df
    df=ri[['Category']]
    cate=[]
    x=''
    cate=df['Category'].unique()
    if (apptype.get() == 1):
        x='FREE'
    else:
        x='PAID'
    if(validate_rating()):
        with open('ratinginstall.csv', 'a', newline='') as f:
            field=["App", "Category", "Rating", "Reviews", "Size", "Installs", "Type", "Price", "Content Rating", "Genres", "Last Updated", "Curent Ver", "Android Ver"]
            writer = csv.DictWriter(f, fieldnames=field)
            writer.writerow({"App":app.get(), "Category":category.get(), "Rating":ratings.get(),  "Reviews":reviews.get(),  "Size":size.get(), "Installs": installs.get(), "Type": x, "Price": price.get(),  "Content Rating":contentrating.get(), "Genres":genres.get(), "Last Updated": lastupdated.get(),  "Curent Ver":currentver.get(), "Android Ver": androidver.get()})
            messagebox.showinfo("Success", "Successfully added to CSV file")
            #new_entry.destroy()
       
 
def enable():
    price.config(state='normal')
    return


def add_records():
    global new_entry, app, category, ratings, reviews, size, installs, apptype, price, contentrating, genres, lastupdated, currentver, androidver
    df = ri[['App','Category','Installs','Last Updated','Content Rating','Genres']] 
    new_entry = Tk()
    new_entry.title("New Entry")
    adjustWindow(new_entry)
    app = StringVar(new_entry)
    category = StringVar(new_entry)
    ratings = StringVar(new_entry)
    reviews = StringVar(new_entry)
    size = StringVar(new_entry)
    installs = StringVar(new_entry)
    apptype = IntVar(new_entry)
    price = StringVar(new_entry)
    contentrating = StringVar(new_entry)
    genres = StringVar(new_entry)
    lastupdated = StringVar(new_entry)
    currentver = StringVar(new_entry)
    androidver = StringVar(new_entry)
    #Label(new_entry, text="Enter a New App Entry ", width="500", height="2", font=("Calibri", 30, 'bold'), fg='white',bg='#174873').pack()
    Label(new_entry, text="", bg='#174873', width='110', height='30').place(x=110, y=120)
    Label(new_entry, text="Application Name", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=130, y=160)
    Application_name=Entry(new_entry, textvariable=app).place(x=300, y=160)
  #  Application_name.bind("<Return>", lambda event: validate(event, "Application_name")) 
   # Application_name.bind("<Tab>", lambda event: validate(event, "Application_name")) 
    Label(new_entry, text="Category", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=130,y=210)
    #c=Entry(new_entry, textvariable=category)
    #c.place(x=300, y=210)
    #category = StringVar()
    cate=[]
    cate=df['Category'].unique()
    droplist = OptionMenu(new_entry, category, *cate)
    droplist.config(width=18, height=1)
    category.set('Choose Your Category')
    droplist.place(x=300, y=210)
    Label(new_entry, text="Ratings", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=130,y=260)
    rat=Entry(new_entry, textvariable=ratings)
    rat.place(x=300, y=260)
#    ratings.bind("<Return>", lambda event: validate(event, "ratings")) 
 #   ratings.bind("<Tab>", lambda event: validate(event, "ratings")) 
    Label(new_entry, text="Reviews", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=130,                                                                                                               y=310)
    rev=Entry(new_entry, textvariable=reviews)
    rev.place(x=300, y=310)
    Label(new_entry, text="Size", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=130,                                                                                                            y=360)
    size=Entry(new_entry, textvariable=size)
    size.place(x=300, y=360)
    Label(new_entry, text="Installs", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=130,                                                                                                                y=410)
    inst=Entry(new_entry, textvariable=installs)
    inst.place(x=300, y=410)
    Label(new_entry, text="Type", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=130,                                                                                                            y=460)
    b1=Radiobutton(new_entry, text="FREE",padx = 20, variable=apptype, value=1,background = "light blue")
    b2=Radiobutton(new_entry, text="PAID",padx = 20, variable=apptype, value=2,background = "light blue",command=enable)
    b1.place(x=250, y=460)
    b2.place(x=350, y=460)
    Label(new_entry, text="Price", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=500,                                                                                                             y=160)
    v = StringVar(new_entry, value='$0')
    price=Entry(new_entry,textvariable=v)
    price.config(disabledbackground="light grey",state='disabled')
    price.place(x=670, y=160)
    Label(new_entry, text="Content Rating", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=500, y=210)
    #contentrating = StringVar()
    crat=[]
    crat=list(df['Content Rating'].unique())
    crat.remove('Unrated')
    droplist = OptionMenu(new_entry, contentrating, *crat)
    droplist.config(width=18, height=1)
    contentrating.set('Choose Content Rating')
    droplist.place(x=670, y=210)
    Label(new_entry, text="Genres", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=500,y=260)
    genre=[]
    genre=list(df['Genres'].unique())
    genre.sort()
    droplist = OptionMenu(new_entry, genres, *genre)
    droplist.config(width=18, height=1)
    genres.set('Choose Your Genre')
    droplist.place(x=670, y=260)
    Label(new_entry, text="Last Updated", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=500, y=310)
    date = StringVar(new_entry, value='01/01/2000')
    lastupdated=Entry(new_entry,textvariable=date)
    lastupdated.place(x=670, y=310)
    Label(new_entry, text="Current Version", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=500, y=360)
    ver=Entry(new_entry, textvariable=currentver)
    ver.place(x=670, y=360)
    Label(new_entry, text="Android Version", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=500, y=410)
    aver=Entry(new_entry, textvariable=androidver)
    aver.place(x=670, y=410)
    Button(new_entry, text='Submit', width=20, font=("Open Sans", 13, 'bold'), bg='brown', fg='white',command=check_entry).place(x=500, y=460)
    new_entry.mainloop()

def validate_review():
    if application.get() != '':
        if trans_review.get() != '':
            if sentiment.get() != 'Choose Your Sentiment':
                if re.match("^(-?(0(\.\d+))|1|-1|0(\.\d+)?)$", senti_polarity.get()):
                    if re.match("^(0(\.\d+)?|1)$", senti_subject.get()):
                        return True
                    else:
                        messagebox.showerror("Error", "Enter Valid Sentiment Subjectivity between 0 nd 1")
                        return False
                else:
                    messagebox.showerror("Error", "Enter Valid Sentiment Polarity between -1 and 1")
                    return False
            else:
                messagebox.showerror("Error", "Select valid Sentiment")
                return False
        else:
            messagebox.showerror("Error", "Enter Valid Review")
            return False
    else:
        messagebox.showerror("Error", "Enter Valid App Name")
        return False

def check_review():
    global review_df
    if(validate_review()):
        with open('reviews.csv', 'a', newline='') as f:
            field=["App", "Translated_Review", "Sentiment", "Sentiment_Polarity", "Sentiment_Subjectivity"]
            writer = csv.DictWriter(f, fieldnames=field)
            writer.writerow({"App":application.get(), "Translated_Review":trans_review.get(), "Sentiment":sentiment.get(),  "Sentiment_Polarity":senti_polarity.get(),  "Sentiment_Subjectivity":senti_subject.get()})
            messagebox.showinfo("Success", "Successfully added to CSV file")
    
def new_review():
    global application, trans_review, sentiment, senti_polarity, senti_subject
    new_review = Tk()
    new_review.title("New Review")
    #adjustWindow(new_review)
    application = StringVar(new_review)
    trans_review = StringVar(new_review)
    sentiment = StringVar(new_review)
    senti_polarity = StringVar(new_review)
    senti_subject = StringVar(new_review)
    Label(new_review, text="Enter a New App Review", width="500", height="2", font=("Calibri", 30, 'bold'), fg='white',bg='#174873').pack()
    Label(new_review, text="", bg='#174873', width='50', height='25').place(x=300, y=120)
    Label(new_review, text="Application", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=320, y=160)
    app=Entry(new_review, textvar=application)
    app.place(x=490, y=160)
    Label(new_review, text="Translated Review", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873',anchor=W).place(x=320, y=210)
    rev=Entry(new_review, textvar=trans_review)
    rev.place(x=490, y=210)
    Label(new_review, text="Sentiment", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873', anchor=W).place(x=320,y=260)
    sent=['Positive','Negative','Neutral']
    droplist = OptionMenu(new_review, sentiment, *sent)
    droplist.config(width=18, height=1)
    sentiment.set('Choose Your Sentiment')
    droplist.place(x=490, y=260)
    Label(new_review, text="Sentiment Polarity", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873',anchor=W).place(x=320, y=310)
    pol=Entry(new_review, textvar=senti_polarity)
    pol.place(x=490, y=310)
    Label(new_review, text="Sentiment Subjectivity", font=("Open Sans", 11, 'bold'), fg='white', bg='#174873',anchor=W).place(x=320, y=360)
    sub=Entry(new_review, textvar=senti_subject)
    sub.place(x=490, y=360)
    Button(new_review, text='Submit', width=15, font=("Open Sans", 13, 'bold'), bg='brown', fg='white',command=check_review).place(x=340, y=410)
    new_review.mainloop()

def q18():
    global fig18
    fig18 = Tk()
    fig18.title("QUESTION 18")
    adjustWindow(fig18)
    Label(fig18, text="Provide an interface to add new data to both the datasets provided.", width="100", height="3",font=("Calibri", 15, 'bold'), fg='white', bg='purple').place(x=0, y=0)
    b1 = Button(fig18, text="HOME PAGE", bg="lightpink", width="10", height="1", font="Calibri", fg='red',command=main_screen).place(x=800, y=670)
    b2 = Button(fig18, text="New App Record", bg="lightblue", width="25", height="1", font="Calibri", fg='red',command=add_records).place(x=200, y=220)
    b3 = Button(fig18, text="Review App", bg="lightblue", width="25", height="1", font="Calibri", fg='red',command=new_review).place(x=600, y=220)
    fig18.mainloop()

def second_screen():
    global screen
    screen = Tk()
    screen.title("Google PlayStore App launch Study")  # mentioning title of the window 
    adjustWindow(screen)  # configuring the window 
    Label(screen, text="Google PlayStore App launch Study", width="500", height="2", font=("Calibri", 30, 'bold'), fg='black', bg='pink').pack() 
    Label(screen, text="", bg='lightblue',width='130', height='110').place(x=40, y=120) # blue background in middle of window 
    Label(screen, text="*What would you like to know about the analized data?",font=("Calibri",20,"bold"), bg='blue', fg='orange').place(x=45, y=120)
    Label(screen, text="*Here are 20 questions for which Answers are provided", font=("Open Sans", 15, 'bold'), bg='blue', fg='lightgreen').place(x=45, y=165) 
    Button(screen, text="1) What is the percentage download in each category on the playstore.  ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q1).place(x=45,y=200) 
    Button(screen, text="2) How many apps have managed to get the following number of downloads \na) Between 10,000 and 50,000\nb) Between 50,000 and 150000\nc) Between 150000 and 500000 d) Between 500000 and 5000000", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white' ,command=q2).place(x=45,y=240)
    Button(screen, text="3) Which category of apps have managed to get the most,least and an average of 2,50,000 downloads atleast. ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q3).place(x=45,y=340)
    Button(screen, text="4) Which category of apps have managed to get the highest maximum average ratings from the users.\nDisplay the result using suaitable visualization tool(s) and also update the data into the database. ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q4).place(x=45,y=380)          
    Button(screen, text="5) What is the number of installs for the following app sizes.\na)Size between 10 and 20 mb\nb) Size between 20 and 30 mb\nc) More than 30 mb ", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q5).place(x=45,y=440)
    Button(screen, text="6) For the years 2016,2017,2018 what are the category of apps that have got the most and  the least downloads.", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q6).place(x=45,y=540)
    Button(screen, text="7) All those apps , whose android version is not an issue and can work with varying devices.\n  what is the percentage increase or decrease in the downloads.", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q7).place(x=45,y=580) 
    Button(screen, text="8) Amongst sports, entertainment,social media,news,events,travel and games,which is the category\nof app that is most likely to be downloaded in the coming years, kindly make a prediction\nand back it with suitable findings.Also update the number of\n of downloads that these categories have received into a database.", font=("Open Sans", 12, 'bold'), bg='#174873', fg='white',command=q8).place(x=45,y=640)        
    Button(screen, text="Next Page",width="8", bg='purple', font=("Open Sans", 12, 'bold'), fg='white',command=nextpage).place(x=900,y=670)

def main_screen():
    global screen, dataset
    screen = Tk() 
    screen.title("Welcome")
    adjustWindow(screen)
    dataset = StringVar()
    Label(screen, text="Welcome To Google PlayStore App launch Study", width='50', height="3", font=("Calibri", 30,'bold'), fg='white', bg='purple', anchor = CENTER).place(x=0, y=0)
    Label(screen, text="", bg='light blue', width='400', height='500').place(x=0, y=100)
    Button(screen, text='Analyze Your Data', width=20, font=("Open Sans", 20, 'bold'), bg='pink', fg='black', command=second_screen).place(x=300, y=200)
    Button(screen, text='Add New Records', width=20, font=("Open Sans", 20, 'bold'), bg='pink', fg='black',command=q18).place(x=300, y=300)
    Button(screen, text='See Reviews', width=20, font=("Open Sans", 20, 'bold'), bg='pink', fg='black', command=q14).place(x=300, y=400)
    Message(screen, text='Project By- \n Dhruvi Kakadiya \n Onkar Pednekar \n Yash Shah', width='1000', font=("Helvetica", 20, 'bold', 'italic'), fg='orange', bg='black', anchor = CENTER).place(x=600, y=580)
    Message(screen, text='Group Name- LUMOS', width='2000', font=("Helvetica", 25, 'bold', 'italic'), fg='lightblue', bg='black', anchor = CENTER).place(x=600, y=500)
   
    screen.mainloop() 

def splash_screen(seconds):
    global screen, dataset
    screen = Tk() 
    screen.title("Splash Screen")
    adjustWindow(screen)
    dataset = StringVar()
    canv = Canvas(screen, width=1000, height=1000,bg='black')
    canv.grid(row=5, column=5)
    img = ImageTk.PhotoImage(Image.open("lumos2.jpg"))  # PIL solution
    canv.create_image(200, 100, anchor=NW, image=img)
    label = Label(image=img)
    label.image = img
  

    time.sleep(30)
    delay = 3  # seconds delay between slides
    screen.update()
    time.sleep(delay)
    screen.destroy() 
    main_screen()
splash_screen(3)

