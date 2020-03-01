from flask import Flask
from flask import render_template, url_for
from flask_wtf import FlaskForm, Form
from wtforms import StringField, RadioField, SubmitField, SelectField, Field
from wtforms.widgets import Input, SubmitInput
from wtforms.validators import Length, DataRequired
from flask import request, redirect
from user_old import *
from Bot import Bot

class StartGameForm(FlaskForm):
    start = StringField('#Start', [Length(min=1, max=25), DataRequired()])
    end = StringField('#End', [Length(min=1, max=25), DataRequired()])

app = Flask(__name__)

first = True
round_limit = 15
count = 0
bot_path = []

start = ''
end = ''
start_header = ''
end_header = ''
list_r = ''
list_l = ''

@app.route('/', methods=['GET','POST'])
def home():
    global bot_path
    bot = Bot(5, 3)
    form = StartGameForm(meta={'csrf': False})
    if form.validate_on_submit():
        user_agent = User(10, 5, form.start.data, form.end.data)
        return redirect(url_for('game',first=True,start=form.start.data,end=form.end.data), code='307')
    return render_template('form.html',form=form)

@app.route('/game', methods=['GET','POST'])
def game():
    global count
    global start
    global end
    global start_header
    global end_header
    global list_r
    global list_l

    # Go button/start end form
    form = StartGameForm(meta={'csrf': False})
    # left and right list forms
    start = request.args.get('start')
    end = request.args.get('end')
    side = request.args.get('side')
    first = request.args.get('first')

    if first:
        list_r = []
        list_r = user_round(end)[1:6]
        list_l = []
        list_l = user_round(start)[1:6]
        first = False

    elif side:
        list_r = []
        list_r = user_round(end)[1:6]

    else:
        list_l = []
        list_l = user_round(start)[1:6]

    start_header = start
    end_header = end

    if form.validate_on_submit() and (form.start.data != start or form.end.data != end): # on click for Go
        count = 0
        return redirect(url_for('game',first=True,start=form.start.data, end=form.end.data, start_header=start_header, end_header=end_header, list_r=list_r, list_l=list_l, count=count), code='307')

    if count >= 15:
        return redirect(url_for('loser'))

    return render_template('game.html', start=start, end=end, form=form, start_header=start_header, end_header=end_header, list_r=list_r, list_l=list_l, count=count)

@app.route('/clicked_left', methods=['GET'])
def clicked_left():
    global count
    count += 1
    hashtag = request.args.get('hashtag')[1:]
    print(hashtag)
    return redirect(url_for('game', first=False, side=0, start=hashtag, end=end, start_header=start_header, end_header=end_header, list_r=list_r, list_l=list_l, count=count), code='307')

@app.route('/clicked_right', methods=['GET'])
def clicked_right():
    global count
    count += 1
    hashtag = request.args.get('hashtag')[1:]
    print(hashtag)
    return redirect(url_for('game', first=False, side=1, start=start, end=hashtag, start_header=start_header, end_header=end_header, list_r=list_r, list_l=list_l, count=count), code='307')

@app.route('/loser', methods=['GET','POST'])
def loser():
    form = StartGameForm(meta={'csrf': False})
    if form.validate_on_submit() and (form.start.data != start or form.end.data != end): # on click for Go
        count = 0
        return redirect(url_for('game',first=True,start=form.start.data, end=form.end.data, start_header=start_header, end_header=end_header, list_r=list_r, list_l=list_l, count=count), code='307')
    return render_template('loser.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
