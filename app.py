from flask import Flask, render_template, request, redirect, url_for
from username import getFromusername, fullUpdate
import gunicorn
import time

app = Flask(__name__)

app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='static/favicon.ico'))


@app.route('/<username>/')
def main(username):
    user = getFromusername(username)
    if user is not None:
        return render_template('index.html', user=user, lbdurl='https://letterboxd.com/')
    return redirect('https://letterboxd.com/pro/')


@app.route('/<username>/update/')
def main_update(username):
    fullUpdate(username)
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


if __name__ == '__main__':
    app.run()
