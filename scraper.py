import twint
import sys
import shutil

c = twint.Config()

c.Username = sys.argv[1]
c.Limit = 20
c.Store_json = True
c.Output = "tweets"
shutil.rmtree("tweets")

twint.run.Search(c)