#Importing the required modules for the project
import streamlit as st
from datetime import date
import UploadData
import Scraping
import ScrapDownload
import UploadedData


st.title('Twitter Scrapping')
st.write("All the datas that you have scrapped will be stored in the name of the tag + Starting Date + Ending.")

#Getting tag to scrap
tag = st.text_input("Tag to Scrap", ).lower()
#Getting Starting date to  scrap
since_d = st.date_input("Since", date.today(), min_value = date(2006, 3, 21), max_value=date.today())
since = since_d.strftime("%Y-%m-%d")#Concerting the date into string
#Getting the Ending date of scrap
until_d = st.date_input("Untill", date.today(), min_value = since_d, max_value=date.today())
until = until_d.strftime("%Y-%m-%d")#Concerting the date into string

Scraping.Scrap(tag, since, until) #Function calling with parameters tag, starting and ending date for scrapping
ScrapDownload.scrap_download()#Calling function to Download scraped data
UploadData.upload_data()#Calling function to Upload data to the database
UploadedData.uploaded_data()#Calling function to view, delete and download data
