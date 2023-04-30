from info import *
import json

with open('credentials.json') as f:
    credentials = json.load(f)

p = GetInfo( credentials['email'], credentials['password'], 2)
p.start()



