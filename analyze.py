import statistics
import pandas as pd
import numpy as np

#bokeh
from bokeh.io import output_file, show
from bokeh.layouts import row, gridplot, grid, column
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

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

# print(dates)
# print(weighted_sentiment)

for i, date in enumerate(dates):
    dates[i] = pd.to_datetime(date, format = "%Y-%m-%d %H:%M:%S")

# print(dates)
x = dates
y = weighted_sentiment


for i, sent in enumerate(weighted_sentiment):
    if sent == 0.0:
        y.pop(i)
        x.pop(i)
print(y)

average = abs(((max(y)*min(y))/2))
print(average)



# output to static HTML file
output_file("lines.html")

# create a new plot with a title and axis labels
p = figure(plot_width = 800, plot_height = 400, title="Weighted Sentiment Over Time", x_axis_label='Date-Time', y_axis_label='Weighted Sentiment', x_axis_type="datetime")

# source = ColumnDataSource(data=dict(
#     x=[min(x), max(x)],
#     y1=[average*2, average*2],
#     y2=[average*-2, average*-2],
# ))
# p.vline_stack(['y1', 'y2'], x='x', source=source)

p.line(x = [min(x),max(x)], y = [average*2, average*2], line_width = 1)
p.line(x = [min(x),max(x)], y = [average*-2, average*-2], line_width = 1)

p.circle(x, y, legend="Tweet Sentiment.", size = 5, color="purple")


total_sentiment = sum(y)
if total_sentiment > average:
    bar_color = "green"
elif total_sentiment < average*-1:
    bar_color = "red"
else:
    bar_color = "grey"

total = figure(plot_width = 400, plot_height = 400, title = "Total Sentiment")

total.vbar(x = [1], width = 0.25, bottom = 0, top = [total_sentiment], color = bar_color)




#show graphs
show(column(p, total))





# print(statistics.mean(sentimentscore))
# print(statistics.mean(magnitudescore))


