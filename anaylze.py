tweets = []
f = open("tweets.txt", "r")
for x in f:
    tweet = x[x.find('>')+2:len(x)-1]
    date = x[20:30]
    tweets.append([date,tweet])

# dates = []
# for i in range(len(tweets)):
#     tweets[i] = tweets[i].split(' ')
#     dates.append(tweets[i][1])
#     for _ in range(5):
#         tweets[i].pop(0)

#     tweets[i] = ' '.join(tweets[i])

# tweets_and_dates = zip(dates, tweets)