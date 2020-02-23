from Bot import *
from get_tweets import *
from sort_hashtags import *
from find_path import *

bot = Bot(4, 3, DEBUG=True)

path = bot.search('furries','nazi')

print(path)
