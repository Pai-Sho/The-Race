from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from Bot import Bot

class MyForm(FlaskForm):
    start = StringField('#Start', validators=[DataRequired()])
    end = StringField('#End', validators=[DataRequired()])


app = Flask(__name__)

count = 0

@app.route('/', methods=('GET', 'POST'))
def home():
    form = MyForm(csrf_enabled=False)
    print('HHHHHHEEEEEERRRRRRRRREEEEEEE')
    global count
    count += 1

    bot = Bot(4, 3, DEBUG=True)
    path = bot.search('trump', 'hitler')
    print(path)
    return render_template('Home.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
