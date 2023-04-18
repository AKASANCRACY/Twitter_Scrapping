Pre-Requisites:

1. Python (Added to environmental path)
2. streamlit, pandas, pymongo, snscrape, langdetect, iso_language_codes, datetime. These all are the python libraries that shoul be available in the system.
3. MongoDB
4. Browser(Example Chrome, FireFox, ect,.)


How to run it?

1. Download the zip file(Twitter_Scrapping-master).
2. Extract the zip file.
3. In the extracted folder "TwitterScraper.py" is the main file other files are subfiles which has function defined to do certain task
4. Open command prompt and move towards the directory where the files are located.
5. Run the command "streamlit run TwitterScraper.py" or "streamlit run .\TwitterScraper.py" in the command prompt after moving towards the files directory.
6. A page will be loaded in the browser or in command prompt or we can manually open the page by accessing the which will be displayed in the command prompt.
Example:
	Local URL: http://localhost:8501
	Network URL: http://192.168.155.158:8501
7. The UI designed for twitter scraping will be displayed
8. The guidence to use the page will be provided in the UI Guide file.


Flow of the pogram:

Data Scraping and Downloading section

1. Initially the main file will import the required modules.
2. The main file will get the tag and data range from the user for scraping.
3. Then it will call the function Scraping.Scrap(tag, since_date, until_date) with arguments tag, starting and ending date for scraping the data from twitter
4. All the scrapped datas will be stored in the name of the tag + Starting Date + Ending in MongoDB.
5. In "Scraping.py" file this fucntion is defined. This function will initially checck whether the data is already exist in database or not.
6. If exist it fetches the data from data base and displays it in the browser, else it will scrap the data and it will store it in database and displays it.
7. It will scrap maximum of 1000 datas in between the range of date.
8. This function ends.
9. Secondly "ScrapDownload.scrap_download()" is called from the main file.
10. In "ScrapDownload.py" file this fucntion is defined. In the UI it shows the list of datas that have been scraped.
11. We have to select a data first and then we have to mark the select box in the UI after selecting the data.
12. Then we can able to view or delete the data. Also we can download the data in two formats(json, csv).
Below the view and delete button in UI we have to select the file format and the only we will have the download button in the UI.
13. After selecting the file format "Download.download(s_db, file_name, Format)" function will be called
14. In "Download.py" file this fucntion is defined, to download file from database it gets database name, file name(Collection name) and file format to download as parameters.
15. Then it will fetch the specified data from the database and encode it in the specified file format and shows the option to download the file.

Data Uploading section

1. Thirdly "UploadData.upload_data()" function will be called from the main program. In "UploadData.py" file this fucntion is defined.
2. It provides the facility to upload the data in the database either in csv or json file format.
3. After uploading the uploaded data will be displayed in the web page.
4. Finally "UploadedData.uploaded_data()" function is called from the main program. In "UploadedData.py" file this fucntion is defined.
5. This function is defined to select uploaded data to view or  delete or to select the fomat of downloading the data.
6. If we select the view option it will fetch the particular data from database and displays it
7. Then we can delete the data and also we can download the data in two formats(json, csv).
Below the view and delete button in UI we have to select the file format and the only we will have the download button in the UI.
8. After selecting the file format "Download.download(s_db, file_name, Format)" function will be called
9. In "Download.py" file this fucntion is defined, to download file from database it gets database name, file name(Collection name) and file format to download as parameters.
10. Then it will fetch the specified data from the database and encode it in the specified file format and shows the option to download the file.
