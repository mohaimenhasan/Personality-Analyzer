import sys
import requests
import json
import twitter
import config


def convert_status_to_pi_content_item(s):
    # My code here
    return {
        'userid': str(s.user.id),
        'id': str(s.id),
        'sourceid': 'python-twitter',
        'contenttype': 'text/plain',
        'language': s.lang,
        'content': s.text,
        'created': s.created_at_in_seconds,
        'reply': (s.in_reply_to_status_id == None),
        'forward': False
    }


twitter_api = twitter.Api(consumer_key=config.twitter_consumer_key,
                          consumer_secret=config.twitter_consumer_secret,
                          access_token_key=config.twitter_access_token,
                          access_token_secret=config.twitter_access_secret,
                          debugHTTP=False)
# users
users = ["Marshmello", "Sam Smith", "ZAYN", "Demi Lovato", "Logic", "Dua Lipa", "Louis Tomlinson", "Justin Bieber", "Cardi B", "Hailee Steinfeld", "Khalid Macklemore", "Camila Cabello",  "Avicii", "Niall Horan", "Skrillex", "Chris Brown", "P!nk", "J Balvin", "XXXTENTACION", "OneRepublic", "Liam Payne", "Lauv", "Blackbear", "Portugal. The Man", "Calvin Harris", "Halsey", "Sabrina", "Carpenter", "Bebe Rexha", "Jax Jones", "Jason Derulo", "French Montana", "CNCO", "R3HAB", "David Guetta", "Thomas Rhett", "Imagine Dragons", "21 Savage", "SZA",  "Jonas Blue", "Lil Uzi Vert", "LANY", "Axwell", "Ingrosso", "Rita Ora", "Charlie Puth", "Lorde", "Maroon 5", "Hedley", "Astrid S", "Chelsea Cutler", "Nina Nesbitt", "Marc E. Bassy", "A R I Z O N A", "Caroline Pennell", "Rachel Platten", "Maty Noyes", "Fifth Harmony", "Jaira Burns",  "ODESZA", "Elohim", "Julia Michaels", "Angus & Julia Stone",  "Why Don't We", "LAYNE", "Kelly Clarkson", "Grace VanderWaal", "Grey",  "Miguel", "Kim Petras", "In Real Life", "Robin Schulz", "Rich Chigga", "Loote", "3LAU", "Bryce Vine", "Liz Huett", "Drake", "G-Eazy", "Anthony Russo",  "Ty Dolla $ign", "Bryson Tiller", "A.CHAL", "Snakehips", "NexXthursday", "Travis Scott", "6LACK", "Tay-K",  "Kendrick Lamar", "Gucci Mane", "Frank Ocean",  "Lil Pump", "Lil Peep", "Bhad Bhabie",  "The Americanos", "Kevin Gates", "Starrah", "Lao Ra", "Vanjess", "ILoveMakonnen", "Nicki Minaj", "Ariana Grande", "B.o.B",  "Gym Class Heroes", "Miley Cyrus",  "Far East Movement", "Pitbull", "Rihanna", "The Wanted", "MKTO", "Beyonce", "Selena Gomez", "Eminem", "Kanye West", "Taio Cruz", "T.I.", "Macklemore & Ryan Lewis", "Kesha", "Katy Perry", "Snoop Dogg", "Icona Pop", "Carly Rae Jepsen", "Lady Gaga", "Bruno Mars", "Owl City", "Mark Ronson", "M83",  "Alicia Keys",  "Adele", "Ed Sheeran",  "Klingande", "Tove Lo", "JOHN.k", "dvsn", "Lil Durk", "Arty Beck",  "Nadine Coyle", "Paul Rey", "Terror Jr", "Bearson", "Aquilo", "TIEKS",  "Anna Of The North", "Michael Jackson", "French Braids", "Charlotte Cardin", "filous", "Hoodie Allen", "Z", "George Michael", "The National", "Foo Fighters", "Ivory Waves", "David Ramirez", "Superorganism",  "ARY",  "Ukiyo", "salute",  "DROELOE", "Alex Adair", "Alice Merton", "Plake Transviolet", "Sara Costa", "Super Duper", "Minke", "Mauwe", "Whethan", "Tash Sultana", "Dean Lewis", "Big Wild", "Emily Warren", "Haux", "BAYNK",  "DJDS", "Allie X", "Griffin Stoller", "Baker Grace", "Billie Eilish Dark Honey"]

 
#userIDs


userNames = []


#all Json

allJson = []

#searching for users
for n in range(0, len(users)):
  searchResult = twitter_api.GetUsersSearch(term=users[n], page=1, count=1)
  for User in searchResult:
      userNames.append(User.screen_name)

print(userNames)

# populating the json list
for m in range(0, len(userNames)):
  handle = userNames[m]
  max_id = None
  statuses = []
  for x in range(0, 16):  # Pulls max number of tweets from an account
      if x == 0:
          statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
                                                         count=200,
                                                         include_rts=False)
          status_count = len(statuses_portion)
          max_id = statuses_portion[status_count - 1].id # get id of last tweet and bump below for next tweet set
      else:
          statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
                                                         count=200,
                                                         max_id=max_id,
                                                         include_rts=False)
          status_count = len(statuses_portion)
          max_id = statuses_portion[status_count -1].id#get id of last tweet and bump below for next tweet set
      for status in statuses_portion:
          statuses.append(status)
  pi_content_items_array = list(map(convert_status_to_pi_content_item, statuses))
  pi_content_items = {'contentItems': pi_content_items_array}
  r = requests.post(config.pi_url + '/v2/profile',
                        auth=(config.pi_username, config.pi_password),
                        headers={
                            'content-type': 'application/json',
                            'accept': 'application/json'
                        },
                        data=json.dumps(pi_content_items)
                        )
  print("Profile Request sent. Status code: %d, content-type: %s" % (r.status_code, r.headers['content-type']))
  A = r.text
  dataFromArtist = json.dumps(A)
  allJson.append(dataFromArtist)


with open('OutputData.txt', 'w') as outfile:
    json.dump(allJson, outfile)