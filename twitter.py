
# coding: utf-8

# In[3]:


import twitter 
# Go to http://dev.twitter.com/apps/new to create an app and get values 
# for these credentials, which you'll need to provide in place of these 
# empty string values that are defined as placeholders. 
# See https://developer.twitter.com/en/docs/basics/authentication/overview/oauth 


# In[ ]:


# for more information on Twitter's OAuth implementation. 
CONSUMER_KEY = 
CONSUMER_SECRET = 
OAUTH_TOKEN = 
OAUTH_TOKEN_SECRET = '' 
auth = twitter . oauth . OAuth ( OAUTH_TOKEN , OAUTH_TOKEN_SECRET , CONSUMER_KEY , CONSUMER_SECRET ) 
twitter_api = twitter . Twitter ( auth = auth ) 


