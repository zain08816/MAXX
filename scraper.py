import twint
import sys
import os

c = twint.Config()

c.Username = sys.argv[1]
c.Limit = 20
c.Output = "tweets.txt"

if os.path.exists("tweets.txt"):
    os.remove("tweets.txt")

twint.run.Search(c)
