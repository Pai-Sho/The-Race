from flask import Flask
from flask import render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import Length
from flask import request, redirect
from user import *
from Bot import Bot

class MyForm(FlaskForm):
    start = StringField('#Start', [Length(min=1, max=25)])
    end = StringField('#End', [Length(min=1, max=25)])

class ListForm(FlaskForm):
    choices = None
    '''
    Class ListForm

    Inputs:
        choices:    list of strings of choices
    '''
    def set_choices(self, choices):
        self.choices = choices

class MyListForm(FlaskForm):
    def __init__(self, choices):
        super().__init__(meta={'csrf': False})
        self.option1 = SubmitField(choices[0])
        self.option2 = SubmitField(choices[1])
        self.option3 = SubmitField(choices[2])
        self.option4 = SubmitField(choices[3])
        self.option5 = SubmitField(choices[4])


app = Flask(__name__)

first = True
round_limit = 15
count = 0
bot_path = []

start_header = ''
end_header = ''

@app.route('/', methods=['GET','POST'])
def home():
    global bot_path
    # instantiate bot
    bot = Bot(5, 3)

    form = MyForm(meta={'csrf': False})
    if form.validate_on_submit():
        # run the search
        #try:
            #bot_path = bot.search(form.start.data, form.end.data)
        #print(form.start.data,form.end.data)
        return redirect(url_for('game',start=form.start.data,end=form.end.data), code='307')
        #except Exception as e:
            ## TODO: use a UI element to say change input
            #print('bad')
    
    return render_template('form.html',form=form)

@app.route('/game', methods=['POST'])
def game(side='l', selected_hashtag=''):
    global count
    count += 1
    # Go button/start end form
    form = MyForm(meta={'csrf': False})
    # left and right list forms
    start = request.args.get('start')
    end = request.args.get('end')

    print('FUCKSHIT',start,end)

    start_list, end_list = None, None
    
    # update the lists depending on the sitution
    if first:
        list_l = user_round(start)
        list_r = user_round(end)
        # create the forms for both start and end
        #start_list = ListForm(meta={'csrf': False})
        #start_list.set_choices(list_l)
        start_list = MyListForm(list_l)

        print('start list',start_list.data)
        #end_list = ListForm(meta={'csrf': False})
        #end_list.set_choices(list_r)
        end_list = MyListForm(list_r)
        print('List 1: {}'.format(list_l))
        print('List 2: {}'.format(list_r))

    else:
        # init lists
        start_list = request.args.get('start_list')
        end_list = request.args.get('end_list')

        
        side = request.args.get('side')
        new_list = user_round(selected_hashtag)
        if side == 'l':
            list_l = new_list
            #start_list = ListForm(meta={'csrf': False})
            #start_list.set_choices(list_l)
            start_list = MyListForm(list_l)
        else:
            list_r = new_list
            #end_list = ListForm(meta={'csrf': False})
            #end_list.set_choices(list_r)
            end_list = MyListForm(list_r)
    
    # check for winning condition
    # if set([start] + start_list.choices).intersection(set([end] + end_list.choices)):
        # WIN
        # return

    # add on click funcitonality
    if start_list.validate_on_submit() and start_list.data != {}:    # on click for left and right
        count += 1
        #render_template('game.html', start=start, end=end, start_list=start_list, end_list=end_list, form=form)
        return redirect(url_for('game',start=start_list.data, end=end), code='307')
    elif end_list.validate_on_submit() and end_list.data != {}:    # on click for left and right
        count += 1
        #render_template('game.html', start=start, end=end, start_list=start_list, end_list=end_list, form=form)
        return redirect(url_for('game',start=start, end=end_list.data), code='307')
    elif form.validate_on_submit() and (form.start.data != start or form.end.data != end): # on click for Go
        count = 0
        return redirect(url_for('game',start=form.start.data, end=form.end.data), code='307')
    return render_template('game.html', start=start, end=end, start_list=start_list, end_list=end_list, form=form)

if __name__ == '__main__':
    app.run(debug=True)
