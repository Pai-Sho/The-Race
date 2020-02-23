from Bot import *
from get_tweets import *
from sort_hashtags import *
from find_path import *
from user import *

START = 'gatorade'
END = 'girlscouts'

bot = Bot(4, 3, DEBUG=True)

print('Bot run')
path = bot.search(START, END)
print(path)

url_path = find_path(path)
print(url_path)
print('URL PATH [0]')
print(url_path[0])
f = []
for i in range(len(url_path)):
    #f.apend(get_tweet_embedding(url_path[i]))
    print(get_tweet_embedding(url_path[i]))



print('user run')
temp = '{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n'
ROUNDS = 10
tags = user_round(START)
print(temp.format(*tags))
while True:
    next_tag = input()
    if next_tag == END and next_tag in tags:
        print('yay')
        break
    ROUNDS -= 1
    if ROUNDS < 1:
        print('oof')
    tags = user_round(next_tag)
    print(temp.format(*tags))
