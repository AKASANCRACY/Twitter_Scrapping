#Importing the required modules for the project
import streamlit as st
import pandas as pd
import pymongo
import Download


#specifying the server address to connect with MongoDB
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
u_db = client["UploadedData"]#Accesing the DataBase created to store uploaded data
select_u_file = u_db["U_File"]#Collection which holds the Selected uploaded file name temporarily

#Function defined to select uploaded data to view, delete and the fomat of downloading the dat
def uploaded_data():
    st.title('Uploaded Data')
    #Creating list of available data to display in ui
    upload_list = u_db.list_collection_names()#Collecting the list of collection in database
    upload_list.sort()#Sorting the list
    if "U_File" in upload_list:
        upload_list.remove("U_File")#Removing the temporary collection name from the list

    #Listing the list in UI
    up_file_name = st.radio("Select Uploaded Data", upload_list)
    state = st.checkbox("Check to Select Data", value = False)#CheckBox in UI to select uploaded data to view or download or delete
    if state == True:
        if up_file_name != None:
            #Deleting the temp file name holder and inserting the new file name
            select_u_file.drop()
            select_u_file.insert_one({"name" : up_file_name})
            st.success(up_file_name + " file is selected")
        else:            
            st.error("No data Selected")
    else:
        st.warning("Check the above box to select data")

    col1, col2, col3 = st.columns(3)#Creating a coloumn in UI to have buttons coloumn wise

    #View button in UI
    if col1.button("View", key = "button") and state == True:
        if up_file_name != None:
            coll = u_db[up_file_name]
            data = list(coll.find())#collecting the datas from the collection and converting into list
            df = pd.DataFrame(data)#Converting the list of data into dataframe
            df = df.drop('_id', axis=1)#Neglecting the object id created by MongoDB for each data
            st.dataframe(df)
        else:
            st.error("No data to View")


    #Delete button in UI
    if col2.button("Delete") and state == True:#Delete button
        if up_file_name != None:
            #Deleting the selected uploaded data from Database
            u_db[up_file_name].drop()
            st.success("Data Deleted Refresh the page")
        else:
            st.error("No data to Delete")

    #Listing the available datafomat to be selected to download
    file_dformat = st.selectbox("Select Download Format",["JSON","CSV"])
    try:
        if st.button("Select", key="Select3") and state == True:
            Download.download(u_db, up_file_name, file_dformat)#Calling the download function to download the data
    except NameError as e:
        st.error("No files Selected")
