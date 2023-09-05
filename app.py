from flask import Flask, render_template, url_for, request, redirect, send_file, send_from_directory, make_response
from username import checkUsername, fullUpdate
from config import *
from mongodb import db
import sys
from utils.collage import collage
from utils.tmdb_new_update import updatefromtmdb, updatePeople, updatePeople2
from threading import Thread
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import os
from utils.allowed import allowed, addAllowed

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300


def logged():
    return request.cookies.get('psw') == adminpsw


@app.route('/<username>/', methods=['POST', 'GET'])
def main(username):
    if username == 'ping':
        return 'ok'
    if '.ico' not in username and 'success' not in username:
        current_year = date.today().year
        current_month = date.today().month
        current_week = 53
        if username.lower() == 'reset':
            sys.exit()
        if username.lower() == 'faq':
            return render_template('faq.html')
        print("requested: " + username.lower())
        user = checkUsername(username.lower())
        if user is None:
            if not allowed(username.lower()):
                return render_template('noallowed.html')
        else:
            if 'update' in user:
                if user['update'] <= datetime.today() - timedelta(days=90):
                    if fullUpdate(username.lower(), False):
                        return redirect("/" + username)
                    else:
                        return render_template('error.html')
                if user['update'] <= datetime.today() - timedelta(days=30):
                    return redirect('/' + username + '/update')
            if 'diary' and 'stats' in user:
                try:
                    return render_template('index.html', user=user, lbdurl='https://letterboxd.com/', roles=crew_html,
                                           year="", yearnum=0, current_year=current_year, current_month=current_month,
                                           current_week=current_week)
                except:
                    pass
        if fullUpdate(username.lower(), False):
            return render_template('index.html', user=checkUsername(username.lower()), lbdurl='https://letterboxd.com/',
                                   roles=crew_html, year="", yearnum=0, current_year=current_year,
                                   current_month=current_month, current_week=current_week)
        else:
            return render_template('error.html')
    return render_template('username.html')


@app.route('/handle_data', methods=['POST', 'GET'])
def handle_data():
    db.Suggestion.insert_one({'name': request.form['name'], 'text': request.form['suggestion']})
    return redirect(url_for('success'))


@app.route('/updatetmdb', methods=['POST', 'GET'])
def updatetmdb2():
    def do_work():
        updatefromtmdb(True)
        #updatePeople(True)
        updatePeople2()

    thread = Thread(target=do_work)
    thread.start()
    return 'started'


@app.route('/login', methods=['POST', 'GET'])
def loginf():
    if request.args['psw'] == adminpsw:
        resp = make_response("loggato!")
        expire_date = datetime.now()
        expire_date = expire_date + timedelta(days=180)
        resp.set_cookie("psw", value=request.args['psw'], expires=expire_date)
        return resp
    return redirect("/")


@app.route('/<username>/<year>', methods=['POST', 'GET'])
def main_year(username, year):
    if '.ico' not in username:
        # if beta_test and username.lower() not in beta_users:
        #    return render_template('username.html')
        current_year = date.today().year
        current_month = 12
        current_week = 53
        if int(year) == int(current_year):
            current_month = date.today().month
            current_week = date.today().isocalendar()[1]
        user = checkUsername(username.lower())
        if user is not None:
            if 'stats_' + str(year) not in user:
                return redirect("/" + username)
            return render_template('index.html', user=user, lbdurl='https://letterboxd.com/', roles=crew_html,
                                   year='_' + year, yearnum=year, current_year=current_year,
                                   current_month=current_month,
                                   current_week=current_week)
        return render_template('loading.html', redirect=(username.lower()))
    return render_template('username.html')


@app.route('/<username>/update/', methods=['POST', 'GET'])
def main_update(username):
    # if beta_test and username.lower() not in beta_users:
    #    return render_template('username.html')
    if not allowed(username.lower()):
        return render_template('noallowed.html')
    if 'last' in request.args:
        last = datetime.strptime(request.args['last'], '%Y-%m-%d')
        last = last + relativedelta(months=3)
        if datetime.today() > last:
            print("Full Update")
            if fullUpdate(username.lower(), False):
                return redirect("/" + username)
            else:
                return render_template('error.html')
    if fullUpdate(username.lower(), True):
        # return render_template('index.html', user=checkUsername(username.lower()), lbdurl='https://letterboxd.com/', roles=crew_html, year="", yearnum=0)
        return redirect("/" + username)
    else:
        return render_template('error.html')


@app.route('/<username>/collage/', methods=['POST', 'GET'])
def main_collage(username):
    if not allowed(username.lower()):
        return render_template('noallowed.html')
    red = collage(username)
    if red is not None:
        return redirect(red, code=302)
    else:
        try:
            return send_file("utils/tmp.jpg", mimetype='image/jpg')
        except:
            return send_file("/tmp/tmp.jpg", mimetype='image/jpg')


@app.route('/<username>/add', methods=['POST', 'GET'])
def add_allowed(username):
    if logged():
        addAllowed(username.lower())
        return redirect('/'+username.lower())
    return redirect('/')


@app.route('/', methods=['POST', 'GET'])
def main_std():
    return render_template('username.html')


@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error_Flask.html', errore="Errore del server"), 500


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')

@app.context_processor
def utility_processor():
    def format_comma(number):
        return f'{int(number):,}'

    return dict(format_comma=format_comma)


@app.context_processor
def utility_processor3():
    def ifNull0_divide2(val):
        if val is None:
            return 0
        else:
            return val / 2

    return dict(ifNull0_divide2=ifNull0_divide2)


@app.context_processor
def utility_processor4():
    def firstUpper(string):
        if len(string) < 4:
            return string.replace('-', ' ').title().upper()
        return string.replace('-', ' ').title().replace('And', 'and').replace('Or', 'or')

    return dict(firstUpper=firstUpper)


@app.context_processor
def utility_processor13():
    def upperJoin(i, t):
        try:
            if t == 'genre':
                string = gen_l[i]
            elif t == 'country':
                string = cou_l[i]
            elif t == 'language':
                string = lan_l[i]
            else:
                return ""
            if len(string) < 4:
                return string.replace('-', ' ').title().upper()
            print(string)
            return string.replace('-', ' ').title().replace('And', 'and').replace('Or', 'or')
        except:
            return i
    return dict(upperJoin=upperJoin)


@app.context_processor
def utility_processor14():
    def lowerJoin(i, t):
        try:
            if t == 'genre':
                string = gen_l[i]
            elif t == 'country':
                string = cou_l[i]
            elif t == 'language':
                string = lan_l[i]
            else:
                return ""
            return string
        except:
            return i
    return dict(lowerJoin=lowerJoin)


@app.context_processor
def utility_processor8():
    def firstUpperBis(string):
        if len(string) < 4:
            return string.replace('-', ' ').title().upper()
        string2 = string.title()
        if "-" in string:
            string = string.split("-")
            string2 = ""
            for stri in string:
                if not stri.isdecimal():
                    if len(stri) == 1:
                        stri = stri + "."
                    elif len(stri) == 2:
                        stri = stri[0] + "." + " " + stri[1] + "."
                    string2 = string2 + stri.title() + " "
            string2 = string2[:-1]
        return string2

    return dict(firstUpperBis=firstUpperBis)


@app.context_processor
def utility_processor5():
    def perctodeg(val):
        return 360 * val

    return dict(perctodeg=perctodeg)


@app.context_processor
def utility_processor6():
    def valtoperc(val):
        return int(val * 100)

    return dict(valtoperc=valtoperc)


@app.context_processor
def utility_processor7():
    def numToStars(num, half=True):
        if num is not None:
            if half:
                num = num / 2
            result = int(num) * "★"
            if num > int(num):
                result = result + "½"
            return result

    return dict(numToStars=numToStars)


@app.context_processor
def utility_processor8():
    def replaceSize(src, height, width):
        if src is not None:
            if 'a.ltrbxd' in src:
                try:
                    return src.rsplit("-0-", 2)[0] + "-0-" + str(height) + "-0-" + str(width) + "-crop.jpg"
                except:
                    print(src)
                    return ""
            else:
                try:
                    return '//a.ltrbxd.com/resized/' + src + "-0-" + str(height) + "-0-" + str(width) + "-crop.jpg"
                except:
                    print(src)
                    return ""

    return dict(replaceSize=replaceSize)


@app.context_processor
def utility_processor9():
    def fill_array(array, min, max):
        array2 = []
        z = 0
        for i in range(min, max + 1):
            try:
                if array[z]['_id'] == i:
                    array2.append(array[z])
                    z = z + 1
                else:
                    array2.append({'_id': i, 'sum': 0})
            except:
                array2.append({'_id': i, 'sum': 0})
        # print(array2)
        return array2

    return dict(fill_array=fill_array)


@app.context_processor
def utility_processor10():
    def date_toshort(date):
        date2 = date.strftime("%b %e")
        return date2

    return dict(date_toshort=date_toshort)


@app.context_processor
def utility_processor11():
    def zeroIfNone(value):
        if value is None:
            return 0
        return value

    return dict(zeroIfNone=zeroIfNone)


@app.context_processor
def utility_processor12():
    def numtomonth(value):
        if value > 0:
            mesinum = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep',
                       10: 'Oct', 11: 'Nov', 12: 'Dec'}
            return mesinum[value]
        else:
            return ''
    return dict(numtomonth=numtomonth)


if __name__ == '__main__':
    app.run()
