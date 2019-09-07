import statistics
import pandas as pd
from bokeh.io import output_file, show
from bokeh.layouts import row
from bokeh.plotting import figure

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()


tweets = []
f = open("tweets.txt", "r")
for x in f:
    x = x.split(' ')
    date = ' '.join(x[1:3])
    tweet = ' '.join(x[5:])
    tweets.append([date, tweet])

print(tweets)    
    
    
     #= x[x.find('>')+2:len(x)-1]
    # date = x[20:39]
    # tweets.append([date,tweet.lower()])



# tweets_and_dates = zip(dates, tweets)

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


weighted_sentiment = [sentimentscore[i]*magnitudescore[i] for i in range(len(magnitudescore))]
dates = [data[0] for data in tweets]

print(dates)
print(weighted_sentiment)

for i, date in enumerate(dates):
    dates[i] = pd.to_datetime(date, format = "%Y-%m-%d %H:%M:%S")

print(dates)
x = dates
y = weighted_sentiment

# create graph

# output to static HTML file
output_file("lines.html")

# create a new plot with a title and axis labels
p = figure(title="Weighted Sentiment Over Time", x_axis_label='Date-Time', y_axis_label='Weighted Sentiment', x_axis_type="datetime")

# add a line renderer with legend and line thickness
p.line(x, y, legend="Tweet Sentiment.", line_width=2)
# show the results
show(p)





# print(statistics.mean(sentimentscore))
# print(statistics.mean(magnitudescore))

# flagged_words = ['kill', 'gun', 'dead', 'suicide', 'shoot', 'hurt', 'depressed']

