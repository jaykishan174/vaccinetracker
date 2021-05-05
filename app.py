# -*- coding: utf-8 -*-
"""
Created on Wed May  5 12:15:31 2021

@author: j.wadhwani
"""

######Code will end you an email if it finds a vaccine appointment within 5 days in your zipcode
import streamlit as st
import requests
import json
from datetime import datetime, timedelta
from playsound import playsound
import time

st.markdown("<h1 style='text-align: center; color: blue;'>COVID 19 18-45 Vaccination Tracker</h1>", unsafe_allow_html=True)

zipcode_num=st.text_input("Enter the zip code")
interval= st.number_input("Enter the Time Interval (In Min)",min_value=0,step=1)

zipcode = zipcode_num #change to your pin code as needed
datelist = []

for i in range(0,5): #can increase range further if you want to check for more than 5 days
    today = datetime.today() + timedelta(i)
    datestr = datetime.strftime(today,'%d-%m-%Y')
    datelist.append(datestr)

age_18 = 0 


row_1_2, row_1_3 = st.beta_columns(2)
button_1= row_1_2.button("Start")
button_2= row_1_3.button("Stop")

while button_1== True:
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    for datestring in datelist:
        headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',}
        r = requests.get('http://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode='+str(zipcode)+'&date='+datestring, headers=headers)
        st.write(r.text)
        resp= json.loads(r.text)
        if len(resp['sessions']) >= 1:
            for x in resp['sessions']:
                if x['min_age_limit'] <= 18:    ##set to 18 or under, can increase to 45 if needed
                    age_18 = age_18 + 1
    
    statement= " at "+zipcode+" checked at "+current_time                
    if age_18 >= 1:
        st.subheader("Vaccine Found"+ statement)
        for i in range(0,5):
            playsound('sound.mp3')    
            
    else:
        st.write("Vaccine Not Found"+ statement)
    if(button_2==True):
        break
    time.sleep(interval*60)
