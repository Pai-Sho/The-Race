from flask import Flask
from flask import render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length
from flask import request, redirect
from user import *
from Bot import Bot
from get_tweets import get_tweets_by_hashtag_pair, get_tweet_embedding
from find_path import find_path
import html

class MyForm(FlaskForm):
    start = StringField('#Start', [Length(min=1, max=25)])
    end = StringField('#End', [Length(min=1, max=25)])



app = Flask(__name__)

count = 0

@app.route('/', methods=['GET','POST'])
def home():
    form = MyForm(meta={'csrf': False})
    if form.validate_on_submit():
        return redirect(url_for('run_bot',start=form.start.data,end=form.end.data), code='307')
    return render_template('form.html',form=form)

@app.route('/game', methods=['POST'])
def game():
    print('howdy')
    form = MyForm(meta={'csrf': False})
    start = request.args.get('start')
    end = request.args.get('end')
    list1 = user_round(start)
    if form.validate_on_submit() and (form.start.data != start or form.end.data != end):
        return redirect(url_for('/game',start=form.start.data, end=form.end.data), code='307')
    return render_template('game.html', start=start, list1=list1, form=form)

@app.route('/run_bot', methods=['POST'])
def run_bot():
    # start bot
    bot = Bot(8, 3, DEBUG=True)
    form = MyForm(meta={'csrf': False})
    start = request.args.get('start')
    end = request.args.get('end')
    # start search
    path = bot.search(start, end)
    # get a path of urls
    url_path = find_path(path)

    shit = ''

    for i in range(len(url_path)):
        shit += get_tweet_embedding(url_path[i])

    tweet_path = []
    for this_url in url_path:
        tweet_path.append(html.unescape(get_tweet_embedding(this_url)))

    if len(tweet_path) == 0:
        tweet_path = ["<div> No path found </div>"]
    
    #tweet_path = ['<blockquote class="twitter-tweet"><p lang="en" dir="ltr">If the election was today who are you voting for on 2/22/2020<a href="https://twitter.com/hashtag/Election2020?src=hash%20amp;ref_src=twsrc%5Etfw">#Election2020</a> <a href="https://twitter.com/hashtag/Trump?src=hash%20amp;ref_src=twsrc%5Etfw">#Trump</a> <a href="https://twitter.com/hashtag/Warren?src=hash%20amp;ref_src=twsrc%5Etfw">#Warren</a> <a href="https://twitter.com/hashtag/PeteButtigieg?src=hash%20amp;ref_src=twsrc%5Etfw">#PeteButtigieg</a> <a href="https://twitter.com/hashtag/Sanders?src=hash%20amp;ref_src=twsrc%5Etfw">#Sanders</a> <a href="https://twitter.com/realDonaldTrump?ref_src=twsrc%5Etfw">@realDonaldTrump</a> <a href="https://twitter.com/SenWarren?ref_src=twsrc%5Etfw">@SenWarren</a> <a href="https://twitter.com/PeteButtigieg?ref_src=twsrc%5Etfw">@PeteButtigieg</a> <a href="https://twitter.com/BernieSanders?ref_src=twsrc%5Etfw">@BernieSanders</a> <a href="https://twitter.com/hashtag/poll?src=hash%20amp;ref_src=twsrc%5Etfw">#poll</a> <a href="https://twitter.com/hashtag/election?src=hash%20amp;ref_src=twsrc%5Etfw">#election</a> <a href="https://twitter.com/hashtag/trump?src=hash%20amp;ref_src=twsrc%5Etfw">#trump</a> <a href="https://twitter.com/hashtag/Bernie2020?src=hash%20amp;ref_src=twsrc%5Etfw">#Bernie2020</a> <a href="https://twitter.com/hashtag/Warren2020?src=hash%20amp;ref_src=twsrc%5Etfw">#Warren2020</a> <a href="https://twitter.com/hashtag/biden?src=hash%20amp;ref_src=twsrc%5Etfw">#biden</a> <a href="https://twitter.com/hashtag/NevadaCaucus?src=hash%20amp;ref_src=twsrc%5Etfw">#NevadaCaucus</a> <a href="https://twitter.com/hashtag/NVCaucus?src=hash%20amp;ref_src=twsrc%5Etfw">#NVCaucus</a> <a href="https://twitter.com/hashtag/Nevada?src=hash%20amp;ref_src=twsrc%5Etfw">#Nevada</a></p>%20mdash; One Day One Poll (@OneDayPoll1) <a href="https://twitter.com/OneDayPoll1/status/1231381919289561088?ref_src=twsrc%5Etfw">February 23, 2020</a></blockquote>\n<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n', '<blockquote class="twitter-tweet"><p lang="en" dir="ltr">If the election was today who are you voting for on 2/22/2020<a href="https://twitter.com/hashtag/Election2020?src=hash%20amp;ref_src=twsrc%5Etfw">#Election2020</a> <a href="https://twitter.com/hashtag/Trump?src=hash%20amp;ref_src=twsrc%5Etfw">#Trump</a> <a href="https://twitter.com/hashtag/Warren?src=hash%20amp;ref_src=twsrc%5Etfw">#Warren</a> <a href="https://twitter.com/hashtag/PeteButtigieg?src=hash%20amp;ref_src=twsrc%5Etfw">#PeteButtigieg</a> <a href="https://twitter.com/hashtag/Sanders?src=hash%20amp;ref_src=twsrc%5Etfw">#Sanders</a> <a href="https://twitter.com/realDonaldTrump?ref_src=twsrc%5Etfw">@realDonaldTrump</a> <a href="https://twitter.com/SenWarren?ref_src=twsrc%5Etfw">@SenWarren</a> <a href="https://twitter.com/PeteButtigieg?ref_src=twsrc%5Etfw">@PeteButtigieg</a> <a href="https://twitter.com/BernieSanders?ref_src=twsrc%5Etfw">@BernieSanders</a> <a href="https://twitter.com/hashtag/poll?src=hash%20amp;ref_src=twsrc%5Etfw">#poll</a> <a href="https://twitter.com/hashtag/election?src=hash%20amp;ref_src=twsrc%5Etfw">#election</a> <a href="https://twitter.com/hashtag/trump?src=hash%20amp;ref_src=twsrc%5Etfw">#trump</a> <a href="https://twitter.com/hashtag/Bernie2020?src=hash%20amp;ref_src=twsrc%5Etfw">#Bernie2020</a> <a href="https://twitter.com/hashtag/Warren2020?src=hash%20amp;ref_src=twsrc%5Etfw">#Warren2020</a> <a href="https://twitter.com/hashtag/biden?src=hash%20amp;ref_src=twsrc%5Etfw">#biden</a> <a href="https://twitter.com/hashtag/NevadaCaucus?src=hash%20amp;ref_src=twsrc%5Etfw">#NevadaCaucus</a> <a href="https://twitter.com/hashtag/NVCaucus?src=hash%20amp;ref_src=twsrc%5Etfw">#NVCaucus</a> <a href="https://twitter.com/hashtag/Nevada?src=hash%20amp;ref_src=twsrc%5Etfw">#Nevada</a></p>%20mdash; One Day One Poll (@OneDayPoll1) <a href="https://twitter.com/OneDayPoll1/status/1231381919289561088?ref_src=twsrc%5Etfw">February 23, 2020</a></blockquote>\n<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n', '<blockquote class="twitter-tweet"><p lang="und" dir="ltr"><a href="https://twitter.com/hashtag/PeteButtigieg?src=hash%20amp;ref_src=twsrc%5Etfw">#PeteButtigieg</a><a href="https://twitter.com/hashtag/NevadaCaucus?src=hash%20amp;ref_src=twsrc%5Etfw">#NevadaCaucus</a><a href="https://twitter.com/hashtag/WinTheEra?src=hash%20amp;ref_src=twsrc%5Etfw">#WinTheEra</a><a href="https://t.co/KwBK7BhXva">https://t.co/KwBK7BhXva</a></p>%20mdash; Kelley Dockrey (@DockreyKelley) <a href="https://twitter.com/DockreyKelley/status/1231624723961802752?ref_src=twsrc%5Etfw">February 23, 2020</a></blockquote>\n<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n', '<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Communist <a href="https://twitter.com/hashtag/Bernie?src=hash%20amp;ref_src=twsrc%5Etfw">#Bernie</a> walking along with his comrades after <a href="https://twitter.com/hashtag/NevadaCaucus?src=hash%20amp;ref_src=twsrc%5Etfw">#NevadaCaucus</a> win, for Warren and Amy who finished 4th and 5th is like 9/11 for them.<a href="https://twitter.com/hashtag/NeverBernie?src=hash%20amp;ref_src=twsrc%5Etfw">#NeverBernie</a> <a href="https://t.co/yMKAi0yWsD">pic.twitter.com/yMKAi0yWsD</a></p>%20mdash; MaC💊 #TheBestIsYetToCome (@RedPillMaC) <a href="https://twitter.com/RedPillMaC/status/1231602857675280386?ref_src=twsrc%5Etfw">February 23, 2020</a></blockquote>\n<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>\n']
    
    embedhtml = shit
    
    print(path)
    if form.validate_on_submit() and (form.start.data != start or form.end.data != end):
        return redirect(url_for('/run_bot',start=form.start.data, end=form.end.data, tweet_list=tweet_path), code='307')
    return render_template('Home2.html',embedhtml=embedhtml, path=path)

if __name__ == '__main__':
    app.run(debug=True)
