from flask import Flask, render_template, url_for, request, redirect
from username import checkUsername, fullUpdate
from config import *
from utils.getUsersList import *
from mongodb import db
import sys
from utils.collage import collage
from flask_compress import Compress
from flask_cdn import CDN

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
#app.config['CDN_DOMAIN'] = 'd2b3jqgdwv2xyj.cloudfront.net'
#CDN(app)
#Compress(app)


@app.route('/<username>/')
def main(username):
    if '.ico' not in username and 'success' not in username:
        if username.lower() == 'reset':
            sys.exit()
        if username.lower() == 'faq':
            return render_template('faq.html')
        if username.lower() == 'contact':
            return render_template('contact.html')
        print("requested: " + username.lower())
        if username.lower() not in users_list:
            return render_template('noallowed.html')
        user = checkUsername(username.lower())
        if (user is not None) and ('diary' in user):
            return render_template('index.html', user=user, lbdurl='https://letterboxd.com/', roles=crew_html, year="", yearnum=0)
        if fullUpdate(username.lower(), False):
            return render_template('index.html', user=checkUsername(username.lower()), lbdurl='https://letterboxd.com/',
                                   roles=crew_html, year="", yearnum=0)
        else:
            return render_template('error.html')
    return render_template('username.html')


@app.route('/handle_data', methods=['POST', 'GET'])
def handle_data():
    db.Suggestion.insert_one({'name': request.form['name'], 'text': request.form['suggestion']})
    return redirect(url_for('success'))


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/<username>/<year>')
def main_year(username, year):
    if '.ico' not in username:
        #if beta_test and username.lower() not in beta_users:
        #    return render_template('username.html')
        user = checkUsername(username.lower())
        if user is not None:
            return render_template('index.html', user=user, lbdurl='https://letterboxd.com/', roles=crew_html, year='_'+year, yearnum=year)
        return render_template('loading.html', redirect=(username.lower()))
    return render_template('username.html')


@app.route('/<username>/update/')
def main_update(username):
    #if beta_test and username.lower() not in beta_users:
    #    return render_template('username.html')
    if fullUpdate(username.lower(), True):
        #return render_template('index.html', user=checkUsername(username.lower()), lbdurl='https://letterboxd.com/', roles=crew_html, year="", yearnum=0)
        return redirect("/"+username)
    else:
        return render_template('error.html')


@app.route('/<username>/collage/')
def main_collage(username):
    return redirect(collage(username), code=302)


@app.route('/')
def main_std():
    return render_template('username.html')


@app.context_processor
def utility_processor():
    def format_comma(number):
        return f'{int(number):,}'
    return dict(format_comma=format_comma)

'''
@app.context_processor
def utility_processor2():
    def format_array(array):
        array2 = []
        for element in array:
            array2.append({'x': element['_id'], 'y': element['sum']})
        return array2
    return dict(format_array=format_array)
'''


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
        if len(string) < 4:
            return string.replace('-', ' ').title().upper()
        return string.replace('-', ' ').title().replace('And', 'and').replace('Or', 'or')
    return dict(firstUpper=firstUpper)


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
        return 360*val
    return dict(perctodeg=perctodeg)


@app.context_processor
def utility_processor6():
    def valtoperc(val):
        return int(val*100)
    return dict(valtoperc=valtoperc)


@app.context_processor
def utility_processor7():
    def numToStars(num, half=True):
        if half:
            num = num/2
        result = int(num) * "★"
        if num > int(num):
            result = result + "½"
        return result
    return dict(numToStars=numToStars)


@app.context_processor
def utility_processor8():
    def replaceSize(src, height, width):
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
        for i in range(min, max+1):
            try:
                if array[z]['_id'] == i:
                    array2.append(array[z])
                    z = z+1
                else:
                    array2.append({'_id': i, 'sum': 0})
            except:
                array2.append({'_id': i, 'sum': 0})
        print(array2)
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


@app.after_request
def add_header(response):
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == '__main__':
    app.run()
    app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='static/favicon.ico'))
