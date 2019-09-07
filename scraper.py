import twint
import sys

c = twint.Config()

c.Username = sys.argv[1]
c.Limit = 100
c.Store_json = True
c.Output = "tweets"

twint.run.Search(c)