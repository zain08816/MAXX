from quart import Quart, escape, request, render_template
import twint
import asyncio

app = Quart(__name__)
loop = asyncio.get_event_loop()
tweets = []

@app.route('/')
async def hello():
    #asyncio.ensure_future(blocking_function())
    return await render_template('home.html')

# async def blocking_function():
#     c = twint.Config()

#     c.Username = "hasanthehun"
#     c.Limit = 20
#     c.Store_object = True
#     c.Store_object_tweets_list = tweets
#     twint.run.Search(c)


if __name__ == '__main__':
    app.run()