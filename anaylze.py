import statistics

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()


tweets = []
f = open("tweets.txt", "r")
for x in f:
    tweet = x[x.find('>')+2:len(x)-1]
    date = x[20:30]
    tweets.append([date,tweet.lower()])

sentimentscore = []
magnitudescore = []


# The text to analyze
for text in tweets:
    text = text[1]
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment
    print()
    print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))
    sentimentscore.append(sentiment.score)
    magnitudescore.append(sentiment.magnitude)

print(tweets)
print(statistics.mean(sentimentscore))
print(statistics.mean(magnitudescore))

# flagged_words = ['kill', 'gun', 'dead', 'suicide', 'shoot', 'hurt', 'depressed']

# dates = []
# for i in range(len(tweets)):
#     tweets[i] = tweets[i].split(' ')
#     dates.append(tweets[i][1])
#     for _ in range(5):
#         tweets[i].pop(0)

#     tweets[i] = ' '.join(tweets[i])

# tweets_and_dates = zip(dates, tweets)