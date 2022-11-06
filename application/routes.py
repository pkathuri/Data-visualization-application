from matplotlib.pyplot import title
from application import app
from flask import render_template,url_for
import pandas as pd
import json 
import plotly
import plotly.graph_objects as go
import time
from time import sleep
import requests
# The home route
# The first dataset containing GDP information about Kenya
def get_df(df):   
    """
    A function that takes in a dataset in json format that is obtained
    from the world Bank data API and converts the required information into a CSV.

    Args:
        df (json):The dataset which is in j 
    Returns:
        A dataframe object
    """
    df=pd.DataFrame(columns=['year','GDP'])
    time.sleep(1)
    for item in response[1]:
        year=item['date']
        gdp_value=item['value']
        df=df.append({'year':year,'GDP':gdp_value},ignore_index=True)
    return df
# Pulling data about the GDP of Kenya since 2015 to 2022
parameters={'format':'json','freq':'Y',}
response=requests.get('http://api.worldbank.org/v2/country/ken/indicator/NY.GDP.MKTP.CD?date=2015:2022',params=parameters).json()
# The second dataset containing GDP information of countries in East Africa
def get_east_africa_df(myjson):
    """
    A function that converts json data containing information of East African
    countries and their GDPs that has been obtained from an api  yo a dataframe. 

    Args:
        myjson (json object): A json object obtained from the world bank api containing
        the countries of east africa and their gdps.

    Returns:
        df_east_africa:A dataframe object that contains the information anout East A frican countries
        DPand their GDP values from 2015-2021.
    """
   
    df_east_africa=pd.DataFrame(columns=['year','GDP','countries'])
    time.sleep(1)
    for item in response2[1]:
         year=item['date']
         gdp_value=item['value']
         country=item['country']['value']
         df_east_africa=df_east_africa.append({'year':year,'GDP':gdp_value,'countries':country},ignore_index=True)
    return df_east_africa
parameters2={'format':'json','freq':'Y'}
response2=requests.get('http://api.worldbank.org/v2/country/tz;ken;ug;rwa;bdi/indicator/NY.GDP.MKTP.CD?date=2015:2022',params=parameters2).json()
# Obtaining the dataset for the population of East Africa
def get_east_africa_population(myjson):
    """
    A function that obtains data of the agricultural sector of East Africa from the world bank api in 
    json format and converts it into a dataframe.

    Args:
        myjson (.json): A json object contains agricultural data for East Africa.

    Returns:
        df_agriculture: A dataframe that contains East Africa's agricultural information.
    """
    df_population=pd.DataFrame(columns=['year','countries','value'])
    time.sleep(1)
    for item in response3[1]:
         year=item['date']
         country=item['country']['value']
         value=item['value']
         df_population=df_population.append({'year':year,'countries':country,'value':value},ignore_index=True)
    return df_population
# The source of the population dataset
params3={'format':'json','freq':'Y'}
response3=requests.get('http://api.worldbank.org/v2/country/tz;ken;ug;rwa;bdi/indicator/SP.POP.TOTL?date=2018:2022',params=params3).json()
# The home route
@app.route('/')
def index():
    # A dataframe of the GDP pf Kenya from 2015
     df=pd.DataFrame(columns=['year','GDP'])
     df=get_df(response)
    # Sorting the GDP values according to the years in ascending order
     df=df.sort_values(by='year',ascending=True)
    # Graph one
    # A line plot that shows the trend of GDP growth of Kenya since 2015
     fig=go.Figure(
        data=go.Scatter(
            x=df.year.tolist(),
            y=df.GDP.tolist(),
            mode='markers+lines'
            
        ),layout={'title':'Kenyas GDP since 2015','template':'plotly_white','autosize':False,'width':700,'height':500,'xaxis_title':'year','yaxis_title':'GDP in USD'}
    )
     fig.update_traces(line=dict(width=2))
    # Converting the file into json then calling the javascript to render the json to the front-end of the web application
     graph1JSON=json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
    #graph two
    
    # Using a function to convert the json object of the API call to a dataframe
     df_east_africa=get_east_africa_df(response2)
    # Lineplots to show the trend of growth of the GDP of the countries of East Africa since 2015
     fig2=go.Figure()
     for country in df_east_africa['countries'].unique():
         df_east_africa_pivot=df_east_africa[df_east_africa['countries']==country].pivot(index='year',columns='countries',values='GDP')
         fig2.add_traces(go.Scatter(x=df_east_africa_pivot.index, y=df_east_africa_pivot[country], mode='lines+markers', name = country)
                   )
         fig2.update_layout({'title':'The growth trend of GDP of East African Countries since 2015','template':'plotly_white','autosize':False,'width':700,'height':500})
         fig2.update_xaxes(title_text="Year")
         fig2.update_yaxes(title_text="GDP in Billions of dollars")
    
     graph2JSON=json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
    
    # graph three
    # A barplot to compare the GDP of East African countries from 2015 to 2021
     fig3=go.Figure()
     for country in df_east_africa['countries'].unique():
         df_east_africa_pivot2=df_east_africa[df_east_africa['countries']==country].pivot(index='year',columns='countries',values='GDP')
         fig3.add_traces(go.Bar(y= df_east_africa_pivot2[country], x=df_east_africa_pivot2.index,  name = country)
                   )
         fig3.update_layout({'title':'The GDP of East African Countries since 2015','template':'plotly_white','autosize':False,'width':700,'height':500})
         fig3.update_xaxes(title_text="Year")
         fig3.update_yaxes(title_text="GDP in Billions of dollars")
    
     graph3JSON=json.dumps(fig3,cls=plotly.utils.PlotlyJSONEncoder)
    #  graph four
    # Applying a  function that obtains the population of countries of East African countries from 2018 to 2021
     df_population=get_east_africa_population(response3).sort_values(by='year',ascending=True)
    # A barplot comparing the population of East Africa from 2018
     fig4=go.Figure()
     for country in df_population['countries'].unique():
         df_population_pivot=df_population[df_population['countries']==country].pivot(index='year',columns='countries',values='value')
         fig4.add_traces(go.Bar(y= df_population_pivot[country], x=df_population_pivot.index,  name = country))
         fig4.update_layout({'title':'The Population of East African Countries since 2018','template':'plotly_white','autosize':False,'width':700,'height':500})
         fig4.update_xaxes(title_text="Year")
         fig4.update_yaxes(title_text="Population")
    
     graph4JSON=json.dumps(fig4,cls=plotly.utils.PlotlyJSONEncoder)
    
    
    
     return render_template('index.html',title="Home",graph1JSON=graph1JSON,graph2JSON=graph2JSON,graph3JSON=graph3JSON,graph4JSON=graph4JSON)
     
     country_list=df_population['countries'].unique().tolist()