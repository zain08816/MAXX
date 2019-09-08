import statistics
import pandas as pd
import numpy as np

#bokeh
from bokeh.io import output_file, show
from bokeh.layouts import row, gridplot, grid, column, layout
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
name = ''
for x in f:
    x = x.split(' ')
    date = ' '.join(x[1:3])
    tweet = ' '.join(x[5:])
    name = x[4]
    tweets.append([date, tweet])

# formatting name
name = name[1:len(name)-1]
name = '@'+name

print(name)
# print(tweets)    
    
    
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

# print(statistics.mean(sentimentscore))
# print(statistics.mean(magnitudescore))


#create the weitghted sentiment scores
weighted_sentiment = [sentimentscore[i]*magnitudescore[i] for i in range(len(magnitudescore))]
dates = [data[0] for data in tweets]

# print(dates)
# print(weighted_sentiment)

for i, date in enumerate(dates):
    dates[i] = pd.to_datetime(date, format = "%Y-%m-%d %H:%M:%S")

# print(dates)
x = dates
y = weighted_sentiment


#remove 0 sentiment items (0 sentiment usually occurs when tweet is a link or image)
for i, sent in enumerate(weighted_sentiment):
    if sent == 0.0:
        y.pop(i)
        x.pop(i)
print(y)

#find average sentiment
average = statistics.mean(y)
half = abs(average/2)

print(average)

#get outliers
positive_outliers_y = []
positive_outliers_x = []
negative_outliers_y = []
negative_outliers_x = []
for i, sent in enumerate(y):
    if sent > average+half:
        positive_outliers_y.append(sent)
        positive_outliers_x.append(x[i])
    if sent < average-half:
        negative_outliers_y.append(sent)
        negative_outliers_x.append(x[i])

# output to static HTML file
output_file("lines.html")

# create a new plot with a title and axis labels

top_title = "Weighted Sentiment Over Time For User: {}".format(name)
p = figure(plot_width = 1200, plot_height = 400, title=top_title, x_axis_label='Date-Time', y_axis_label='Weighted Sentiment', x_axis_type="datetime")

#plot average range
p.line(x = [min(x),max(x)], y = [average+half, average+half], line_width = 1)
p.line(x = [min(x),max(x)], y = [average, average], legend = 'Average Line', line_width = 2, color = 'black')
p.line(x = [min(x),max(x)], y = [average-half, average-half], line_width = 1)

#plot graph circles
p.circle(x, y, legend="Tweet Sentiment", size = 7, color="purple")
p.circle(positive_outliers_x, positive_outliers_y, size = 10, color="green")
p.circle(negative_outliers_x, negative_outliers_y, size = 10, color="red")
p.line(x, y, line_width = 1,  color = "pink")

#change total sentiment colors
total_sentiment = sum(y)
if total_sentiment > average:
    bar_color = "green"
elif total_sentiment < average:
    bar_color = "red"
else:
    bar_color = "grey"

total = figure(plot_width = 200, plot_height = 400, title = "Total Sentiment")
total.vbar(x = [1], width = 0.25, bottom = 0, top = [total_sentiment], color = bar_color)

compare = figure(plot_width = 200, plot_height = 200, title = "Negative Outliers vs Positive Outliers")
compare.vbar(x = [0], width = 0.25, bottom = 0, top = [len(negative_outliers_y)], color = 'red')
compare.vbar(x = [0.3], width = 0.25, bottom = 0, top = [len(positive_outliers_y)], color = 'green')

average = figure(plot_width = 200, plot_height = 200, title = "Average Sentiment and Average Magnitude")
average.vbar(x = [0], width = 0.25, bottom = 0, top = [statistics.mean(sentimentscore)], color = 'blue')
average.vbar(x = [0.3], width = 0.25, bottom = 0, top = [statistics.mean(magnitudescore)], color = 'purple')


#show graphs
l = layout([
    [p],
    [total, compare, average]
], sizing_mode = 'stretch_both')
show(l)







