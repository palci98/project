#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import json

def get_data(page):

  data_list = {}
  for i, item in enumerate(page, start=1):
    dictionary = {}
    
    dictionary["departure"] = item.find_all("strong",{"class":"name"})[0].text
    dictionary["destination"] = item.find_all("strong",{"class":"name"})[1].text
      
    if len(item.find_all("p",{"class":"reset time"})) == 2:
      dictionary["departure_time"] = item.find_all("p",{"class":"reset time"})[0].text
      dictionary["destination_time"] = item.find_all("p",{"class":"reset time"})[1].text

    elif len(item.find_all("p",{"class":"reset time color-red"})) == 2:
      dictionary["departure_time"] = item.find_all("p",{"class":"reset time color-red"})[0].text
      dictionary["destination_time"] = item.find_all("p",{"class":"reset time color-red"})[1].text  
    
    else:
    
      if (item.find_all("p",{"class":"reset time color-red"})[0].text < item.find_all("p",{"class":"reset time"})[0].text):  
        dictionary["departure_time"] = item.find_all("p",{"class":"reset time"})[0].text
        dictionary["destination_time"] = item.find_all("p",{"class":"reset time color-red"})[0].text  
      
      else:
        dictionary["destination_time"] = item.find_all("p",{"class":"reset time color-red"})[0].text  
        dictionary["departure_time"] = item.find_all("p",{"class":"reset time"})[0].text
    
    data_list[i] = dictionary
  
  return data_list

def get_connection(source, destination, date, time):

  url = "https://cp.hnonline.sk/vlakbusmhdsk/spojenie/"
  page = requests.get(url)
  soup = BeautifulSoup(page.content, 'html.parser')

  post_params = {'From': source, 'To': destination, 'Date': date, 'Time': time}
  response = requests.post(url, data=post_params)
  soup = BeautifulSoup(response.text, 'html.parser')
  if soup.find_all("b",{"class":"center"}):
    raise ValueError("Not supported date")
  page_div = soup.find_all("div",{"class":"outside-of-popup"})
  
  return page_div