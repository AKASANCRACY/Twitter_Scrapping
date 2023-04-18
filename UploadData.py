#Importing the required modules for the project
import streamlit as st
import pandas as pd
import pymongo
import json
import io


#specifying the server address to connect with MongoDB
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
u_db = client["UploadedData"]#Accesing the DataBase created to store uploaded data
select_u_file = u_db["U_File"]#Collection which holds the Selected uploaded file name temporarily

#Function defined to upload data to database
def upload_data():
    st.title('Upload Data')#Setting title in UI
    up_file = st.file_uploader("", accept_multiple_files=False)#Uploader in UI

    #Listing the available datafomat in which the data can be uploaded and the format must be selected
    up_format = st.selectbox("Select File Uploading Format",["JSON","CSV"])
    upload_list = u_db.list_collection_names()#Creating a list that has the uploaded file names

    if "U_File" in upload_list:
        upload_list.remove("U_File")#Removing the temporary collection from the list

    try:
        up_name = up_file.name.lower()
        if up_name in upload_list:#Checking if the file name already exist in database
            st.error("A file with the same name already exist Please rename the file!")
        elif up_format == "CSV" and st.button("Upload"):
            try:
                #uploading the file if the specified format is CSV
                up_df = pd.read_csv(up_file)
                upload_data = up_df.to_dict(orient='records')
                upload_db = u_db[up_name]
                upload_db.insert_many(upload_data)#Inserting the data in database
                st.write(up_name)
                st.dataframe(up_df)#Displaying the data in UI
            except ValueError:
                st.write("Select file first")
            except TypeError:
                st.error("Upload a CSV File or select the correct format")
            except AttributeError:
                st.warning("Browse the file first")
        elif up_format == "JSON" and st.button("Upload"):
            try:
                #uploading the file if the specified format is JSON
                upload_data = json.load(up_file)
                up_df= pd.DataFrame(upload_data)
                dic = up_df.to_dict(orient='records')
                upload_db = u_db[up_name]
                upload_db.insert_many(dic)#Inserting the data in database
                st.write(up_name)
                st.dataframe(up_df)#Displaying the data in UI 
            except AttributeError:
                st.warning("Browse the file first")
            except json.JSONDecodeError as e:
                st.error("Upload a JSON File or select the correct format")
    except AttributeError:
                st.warning("Browse the file first")
