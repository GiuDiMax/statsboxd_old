from flask import Flask, render_template, request, redirect, url_for
from username import getFromusername, fullUpdate
import gunicorn
import time
from setCollections import mainSetCollection2
from setPeople import mainSetNames2
from setLists import updateLists

app = Flask(__name__)

@app.route('/<username>/')
def main(username):
    if '.ico' not in username:
        if username.lower() == 'adminupdate':
            mainSetNames2()
            mainSetCollection2()
            updateLists()
            return render_template('username.html')
        user = getFromusername(username.lower())
        if user is not None:
            if 'stats' in user:
                return render_template('index.html', user=user, lbdurl='https://letterboxd.com/')
            else:
                return redirect('/'+username+"/update/")
    return redirect('https://letterboxd.com/pro/')


@app.route('/<username>/update/')
def main_update(username):
    fullUpdate(username.lower())
    return redirect('/' + username)


@app.route('/')
def main_std():
    return render_template('username.html')


@app.context_processor
def utility_processor():
    def format_comma(number):
        return f'{int(number):,}'
    return dict(format_comma=format_comma)


@app.context_processor
def utility_processor2():
    def format_array(array):
        array2 = []
        for element in array:
            array2.append({'x': element['_id'], 'y': element['sum']})
        return array2
    return dict(format_array=format_array)


@app.context_processor
def utility_processor3():
    def ifNull0_divide2(val):
        if val is None:
            return 0
        else:
            return val/2
    return dict(ifNull0_divide2=ifNull0_divide2)


@app.context_processor
def utility_processor4():
    def firstUpper(string):
        return string.replace('-', ' ').title()
    return dict(firstUpper=firstUpper)


if __name__ == '__main__':
    app.run()
    app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='static/favicon.ico'))
