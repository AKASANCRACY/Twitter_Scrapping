#Importing the required modules for the project
import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
from langdetect import detect
from iso_language_codes import language_name

#specifying the server address to connect with MongoDB
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
s_db = client["TwitterScrape"]#Accesing the DataBase created to store Scraped data
select_d_file = s_db["S_File"]#Collection which holds the Selected Scraped file name temporarily

#Function defined to Scrape data from twitter
def Scrap(tag, since, until):#The parameters are tag, starting and ending date for scrapping
    if st.button("Scrap Tweets"):#Button in UI for scrapping
        try:
            collection_list=s_db.list_collection_names()
            collection_name = tag+" "+since+" to "+until
            collection = s_db[collection_name]#Creating the collection in the name of tag+" "+since_date+" to "+until_date
            if collection_name in collection_list:#Checking the data to be scraped is whether already present in database
                #If presents the the data is fetched from MongoDB and displayed in UI
                data = list(collection.find())
                df = pd.DataFrame(data)
                df = df.drop('_id', axis=1)
                st.markdown("## Tweets of "+tag)
                st.write("The data is stored in the name "+collection_name+".")
                st.dataframe(df)#Displaying the data in UI
            else:
                #If not then the datas are scraped using snscrape
                #Empty list are created to store the scraped datas temporarily
                tweet_date=[]
                tweet_id=[]
                tweet_con=[]
                tweet_user=[]
                tweet_lang = []
                retweet_count = []
                reply_count = []
                like_count = []
                for i,tweet in enumerate(sntwitter.TwitterSearchScraper('#'+tag+' since:'+since+' until:'+until).get_items()):#Loop for scraping data
                    if i>1000:
                        break
                    j = tweet.date
                    tweet_date.append(str(j))
                    tweet_id.append(str(tweet.id))
                    try:
                        tweet_lang.append(language_name(detect(tweet.content)))
                    except:
                        tweet_lang.append(tweet.lang)

                    retweet_count.append(tweet.retweetCount)
                    reply_count.append(tweet.replyCount)
                    like_count.append(tweet.likeCount)
                    tweet_con.append(tweet.content)
                    tweet_user.append(tweet.user.username)
                #Creating DataFrame with the datas in temp list
                df = pd.DataFrame({"Date" : tweet_date,  "User" : tweet_user, "Tweet ID" : tweet_id, "Content" : tweet_con,
                                    "Language" : tweet_lang, "Likes" : retweet_count, "Reply Count" : reply_count, "Retweet Count" : retweet_count})
                scrap_data = df.to_dict(orient='records')
                collection.insert_many(scrap_data)#Storing the scraped data in MongoDB
                st.markdown("## Tweets of "+tag)
                st.write("The data is stored in the name "+collection_name)
                st.dataframe(df)#Displaying the Scraped data in UI
        except Exception as e:
                st.error("Provide The appropriate details to scrap Tweets!")
                st.error("check your network strength and conectivity")
