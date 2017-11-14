import sys
import requests
import json
import twitter
import config

users = ["Demi Lovato",  "Lorde", "Alan Walker", "Kanye West", "Hailee Steinfeld", "Neck Deep", "The Used", "Knuckle Puck", "With Confidence", "Coldfront"," Keith Urban", "Kelsea Ballerini", "Sam Hunt", "Darius Rucker", "Pink Floyd", "Kansas", "Queen", "Saint Motel", "Cemetery Sun"]
userNames = []


twitter_api = twitter.Api(consumer_key=config.twitter_consumer_key,
                          consumer_secret=config.twitter_consumer_secret,
                          access_token_key=config.twitter_access_token,
                          access_token_secret=config.twitter_access_secret,
                          debugHTTP=False)


#searching for users
totalUsers = []
for n in range(0, len(users)):
  searchResult = twitter_api.GetUsersSearch(term=users[n], page=1, count=1)
  totalUsers.append(searchResult)
  for User in searchResult:
      userNames.append(User.screen_name)

print(totalUsers)