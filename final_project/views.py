from django.shortcuts import render
import requests
import json
from decimal import Decimal
from . import forms

def home_view(request):

#call the API (originally I had multiple links because more than 700 records)
    links=["https://data.gov.sg/api/action/datastore_search?resource_id=96e66346-68bb-4ca9-b001-58bbf39e36a7"]
    for url in links:
        resp=requests.get(url)
        rawdata = resp.json()
        data=[]

#iterate through the data + slice and decimal + create and append to list of lists
    for row in rawdata['result']['records']:
        datarow=[]
        year=row["month"][0:4]
        temperature=Decimal(row["max_temperature"])
        datarow.append(year)
        datarow.append(temperature)
        data.append(datarow)

#create function to find max temperature
    def max_temp(inputlist,year):
        temperatures = []
        for sublist in inputlist:
            if sublist[0] == year:
                temperatures.append(sublist[1])
        return max(temperatures)

#place the years in a set to remove duplicates
    yearcount=set([])
    for sublist in data:
        yearcount.add(sublist[0])

#use the max_temp function and print only the maximum temp for each unique year
    onlymax=[]
    for year in yearcount:
        onlymaxrow=[]
        onlymaxrow.append(year)
        onlymaxrow.append(max_temp(data,year))
        onlymax.append(onlymaxrow)


#sort and print the list of lists
    data=sorted(onlymax)
    



    form = forms.FilterForm(data=request.GET)
    if form.is_valid():
        final_data=[]
        search1=form.cleaned_data.get("from_year")
        search2=form.cleaned_data.get("to_year")
        for item in data:
            if int(item[0]) in range(search1,search2+1):
                final_data.append(item)
        data=final_data
    
   

    

    ctx = {'data': data,
          'form':form,
        
    }

    return render(request,'home_view.html', ctx)




