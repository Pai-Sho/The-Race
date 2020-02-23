from Bot import *
from get_tweets import *
from sort_hashtags import *
from find_path import *
from user import *

START = 'furries'
END = 'nazi'

bot = Bot(4, 3, DEBUG=True)

print('Bot run')
path = bot.search(START, END)
print(path)

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