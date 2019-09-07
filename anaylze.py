tweets = []
f = open("tweets.txt", "r")
for x in f:
    #print(x.find('>'))
    tweet = x[x.find('>')+2:len(x)-1]
    date = x[20:30]
    tweets.append([date,tweet])
