#Importing the required modules for the project
import Download
import streamlit as st
import pymongo
import pandas as pd

#specifying the server address to connect with MongoDB
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
s_db = client["TwitterScrape"]#Accesing the DataBase created to store Scraped data
select_d_file = s_db["S_File"]#Collection which holds the Selected Scraped file name temporarily

#Function defined to select scraped data and the fomat of downloading the data
def scrap_download():
    st.title('Download Scraps')#Setting title in UI
    #Creating list of available data to display in ui
    scrap_list = s_db.list_collection_names()#Collecting the list of collection in database
    scrap_list.sort()#Sorting the list
    if "S_File" in scrap_list:
        scrap_list.remove("S_File")#Removing the temporary collection name from the list
    file_name = st.radio("Select Data", scrap_list)#Listing the Scraped data list
    col1, col2, col3 = st.columns(3)#Creating a coloumn in UI to have buttons coloumn wise
    checked = col1.checkbox("Select", value = False)#CheckBox in UI to select scraped data to download or delete

    #View button in UI
    if col2.button("View") and checked == True:
        if file_name != None:
            coll = s_db[file_name]
            data = list(coll.find())#collecting the datas from the collection and converting into list
            df = pd.DataFrame(data)#Converting the list of data into dataframe
            df = df.drop('_id', axis=1)#Neglecting the object id created by MongoDB for each data
            st.dataframe(df)
        else:
            st.error("No data to View")
    
    #Delete optioin to delete the selected file
    if col3.button("Delete", key = "One") and checked == True:
        if file_name != None:
            if checked == True:
                s_db[file_name].drop()
                st.success("Data Deleted Refresh the page")
            else:
                st.warning("Check the above box to select data")
        else:
            st.error("No data to Delete")
    #Checking whether the file is selected or not
    if checked == True:
        if file_name == None:
            st.error("No data Selected")
        else:
            #Deleting the temp file name holder and inserting the new file name
            st.success("Data Selected")
            select_d_file.drop()
            select_d_file.insert_one({"name" : file_name})
    else:
        st.warning("Check the above box to select data")
    
    #Listing the available datafomat to be selected to download    
    Format = st.selectbox("Select File Format",["JSON","CSV"])
    
    if st.button("Select", key="Select2") and checked == True:
        file_name = str(select_d_file.distinct("name")[0])
        Download.download(s_db, file_name, Format)#Calling the download function to download the data
