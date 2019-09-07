import twint
import sys
import shutil
import os

c = twint.Config()

c.Username = sys.argv[1]
c.Limit = 20
c.Store_json = True
c.Output = "tweets"

if os.path.exists("tweets/tweets.json"):
    shutil.rmtree("tweets")

twint.run.Search(c)
