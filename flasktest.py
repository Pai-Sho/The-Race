from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    start = StringField('#Start', validators=[DataRequired()])
    end = StringField('#End', validators=[DataRequired()])


app = Flask(__name__)

count = 0

@app.route('/', methods=('GET', 'POST'))
def home():
    form = MyForm(csrf_enabled=False)
    print('HHHHHHEEEEEERRRRRRRRREEEEEEE')
    if form.validate_on_submit():
        start = form.start.data
        end = form.end.data
        print(start,end)
        print('WTF')
    global count
    count += 1
    return render_template('Home.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
