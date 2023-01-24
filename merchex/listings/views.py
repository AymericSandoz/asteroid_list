from django.shortcuts import render

# Create your views here.

# ~/projects/django-web-app/merchex/listings/views.py

from django.http import HttpResponse
from django.shortcuts import render
import requests
import pandas as pd
from pandas import json_normalize
from .forms import DateForm
import datetime as datetime

def info(request):
     return render(request,
        'listings/info.html')


#Option: Function that takes a list of asteroids as a parameter and returns this list of asteroids with the next approach to earth for each of these asteroids
#Not used in current version
# def get_next_approach(near_earth_objects):
#     for key, value in near_earth_objects.items():
#                 for asteroid in value:
#                     url_api=f'https://api.nasa.gov/neo/rest/v1/neo/{asteroid["id"]}?api_key=lkU4tlO9nq6DMmRHmd8yWXz6h5kJL2cwQ6QZa6BC'   
#                     req = requests.get(url_api)
#                     response=req.json()
#                     #convert to dataframe for easier sorting
#                     response = json_normalize(response["close_approach_data"])

#                     #only keep future approaches
#                     today=datetime.date.today()
#                     close_approach_dates=response['close_approach_date']
#                     close_approach_dates = pd.to_datetime(close_approach_dates).dt.date
                    
#                     future_close_approach_dates = response.loc[(close_approach_dates >= today)]
#                     future_close_approach_dates=future_close_approach_dates.reset_index(drop = True)
                    
#                     #add next approach to 
#                     if future_close_approach_dates['close_approach_date'].empty!=True:
#                         asteroid["next_approach"]=future_close_approach_dates['close_approach_date'].iloc[0]
                        

#     return near_earth_objects


def get_asteroids(request):
    
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DateForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            #Check if difference of day is lower ou equal to 7 
            diffDays=form.cleaned_data["end_date"]-form.cleaned_data["start_date"]
            if(diffDays.days>7):
                error= f"La différentes entre les 2 dates ({diffDays.days} jours) est supérieur à 7 jours."
                return render(request, 'listings/home.html', {'form': form,"error":error})
            


            start_date=form.cleaned_data["start_date"]
            end_date=form.cleaned_data["end_date"]
            api_key="lkU4tlO9nq6DMmRHmd8yWXz6h5kJL2cwQ6QZa6BC"
            url_api=f'https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}'
            req = requests.get(url_api)
            response = req.json()
            near_earth_objects=response["near_earth_objects"]
          
            
            #Option not used in the current version allowing to directly display the next approach towards the earth of each of the planets
            # near_earth_objects=get_next_approach(near_earth_objects)
        
            context={"near_earth_objects":near_earth_objects}
            
            return render(request, 'listings/asteroids.html',context)
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DateForm()

    return render(request, 'listings/home.html', {'form': form})



def get_asteroid_last_5_approaches(request, asteroid_id,asteroid_name):
    
    url_api=f'https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key=lkU4tlO9nq6DMmRHmd8yWXz6h5kJL2cwQ6QZa6BC'
    req = requests.get(url_api)
    response = req.json()
    
    #convert to dataframe for easier sorting
    response = json_normalize(response["close_approach_data"])

    #only keep previous approaches
    today=datetime.date.today()
    response['close_approach_date'] = pd.to_datetime(response['close_approach_date']).dt.date
    filtered_df = response[response['close_approach_date']<today]

    #keep 5 last approaches and relevant columns
    column_number_start=filtered_df.shape[0]-5
    column_number_end=filtered_df.shape[0]
    asteroid_approaches_df=filtered_df.loc[column_number_start:column_number_end,["close_approach_date","miss_distance.lunar"]]
    
    #Convert date to str
    asteroid_approaches_df["close_approach_date"]= asteroid_approaches_df["close_approach_date"].astype(str)

    #Convert data to list
    asteroid_approaches_list=asteroid_approaches_df.values.tolist()
    

  
    context={"asteroid_information":asteroid_approaches_list,"asteroid_name":asteroid_name}

                
    return render(request,
        'listings/asteroid.html'
        ,context)


