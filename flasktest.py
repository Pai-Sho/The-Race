from flask import Flask
from flask import render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length
from flask import request, redirect
from user import *

class MyForm(FlaskForm):
    start = StringField('#Start', [Length(min=1, max=25)], default='Bananas')
    end = StringField('#End', [Length(min=1, max=25)], default='EpsteinDidntKillHimself')



app = Flask(__name__)

count = 0

@app.route('/', methods=['GET','POST'])
def home():
    form = MyForm(meta={'csrf': False})
    if form.validate_on_submit():
        return redirect(url_for('game',start=form.start.data,end=form.end.data), code='307')
    return render_template('form.html',form=form)

@app.route('/game', methods=['POST'])
def game():
    start = request.args.get('start')
    end = request.args.get('end')
    #print(start, type(start))
    list1 = user_round(start)
    #print('list1:', list1)
    #a = user_round()
    return render_template('game.html', start=start, list1=list1)

'''
@app.route('/', methods=('GET', 'POST'))
def home():
    form = MyForm(csrf_enabled=False)
    print('HHHHHHEEEEEERRRRRRRRREEEEEEE')
    if form.validate_on_submit():
        start = form.start.data
        end = form.end.data
        print(start,end)
        print('WTF')
        return redirect(url_for('game'))
    global count
    count += 1

    bot = Bot(4, 3, DEBUG=True)
    path = bot.search('trump', 'hitler')
    print(path)
    return render_template('Home.html', form=form)

@app.route('/gamestart', methods=('GET','POST'))
def gamestart():
    stuff = request.args()
    print(stuff)
    print('REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
    return render_template('gamestart.html', stuff = stuff)
'''

if __name__ == '__main__':
    app.run(debug=True)
