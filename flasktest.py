from flask import Flask
from flask import render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length
from flask import request, redirect
from user import *

class MyForm(FlaskForm):
    start = StringField('#Start', [Length(min=1, max=25)])
    end = StringField('#End', [Length(min=1, max=25)])



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
    form = MyForm(meta={'csrf': False})
    start = request.args.get('start')
    end = request.args.get('end')
    list1 = user_round(start)
    if form.validate_on_submit() and (form.start.data != start or form.end.data != end):
        return redirect(url_for('game',start=form.start.data, end=form.end.data), code='307')
    return render_template('game.html', start=start, list1=list1, form=form)

if __name__ == '__main__':
    app.run(debug=True)
