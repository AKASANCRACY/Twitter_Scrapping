#Importing the required modules for the project
import streamlit as st
import pandas as pd
import pymongo
import json
import io
#specifying the server address to connect with MongoDB
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/myapp')


#Function to download file from database which gets database name, file name(Collection name) and file format to download
def download(database, file_name, file_format):
    try:
        collection = database[file_name]
        data = list(collection.find())#collecting the datas from the collection and converting into list
        data_frame = pd.DataFrame(data)#Converting the list of data into dataframe
        data_frame = data_frame.drop('_id', axis=1)#Neglecting the object id created by MongoDB for each data
        #Checking the file format and converting the dataframe into the specified file format
        if file_format == "JSON":
            j_data = data_frame.to_json()
            #Download option will be enabled to download json file
            st.download_button("DOWNLOAD", data = j_data, file_name = file_name+".json", mime="application/json")
        elif file_format == "CSV":
            output = io.BytesIO()
            data_frame.to_csv(output, encoding='utf-8', index=False)
            output.seek(0)
            #Download option will be enabled to download csv file
            st.download_button(label = "DOWNLOAD", data = output, file_name = file_name+".csv", mime="text/csv")
    except Exception as e:
        st.write("No Data to download! You forget to mark the select button or No data have been selected")

