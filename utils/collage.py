from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import requests
from mongodb import db
from datetime import date, timedelta, datetime
import base64
import json
from username import get_watched


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, "white")
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


def collage(username):
    get_watched(username, True, True, True)
    month = datetime.now().month
    year = datetime.now().year
    if month > 1:
        year2 = date.today().year
        month2 = month - 1
    else:
        year2 = date.today().year - 1
        month2 = 12

    a = db.Users.aggregate([
        {'$match': {"_id": username}},
        {'$project': {'_id': 0, 'diary2': 1}},
        {'$unwind': '$diary2'},
        #{'$match': {"diary2.date": {'$gte': datetime(year2, month2, 1, 0, 0)}}},
        #{'$match': {"diary2.date": {'$lt': datetime(year, month, 1, 0, 0)}}},
        {'$sort': {'diary2.date': 1}},
        {'$lookup': {
            'from': 'Film', 'localField': 'diary2.id',
            'foreignField': '_id', 'as': 'info'}},
        {'$project': {'id': '$diary2.id', 'like': '$diary2.dLike', 'rating': '$diary2.dRating',
                      'rewatch': '$diary2.rewatch', 'img': {'$first': '$info.images.poster'}}}
    ])
    films = []
    for x in a:
        films.append(x)
    number = len(films)

    #img = Image.open(requests.get('https://wallpaperaccess.com/full/1554870.jpg', stream=True).raw).convert("RGBA")
    #img = img.resize((1080, 1920))
    if __name__ == '__main__':
        img = Image.open("sfondo.jpg").convert("RGBA").resize((1080, 1920))
    else:
        img = Image.open("./utils/sfondo.jpg").convert("RGBA").resize((1080, 1920))
    combined = img
    bordistandard = 25

    if number <= 9:
        j, j2 = 3, 3

    elif number <= 16:
        j, j2 = 4, 4

    elif number <= 25:
        j, j2 = 5, 5

    elif number <= 36:
        j, j2 = 6, 6

    elif number <= 49:
        j, j2 = 7, 7

    elif number <= 64:
        j, j2 = 8, 8

    elif number <= 82:
        j, j2 = 9, 9

    else: j, j2 = 10, 10

    length = int(((1080-(bordistandard*2))/j)*0.85)
    height = int(length*1.5)
    bordioriz = int(length*0.15)
    bordivert = int(height*0.30)
    bordiestremi = int((1080 - (length*j) - bordioriz*(j-1))/2)
    bordoalto = int(1920 - (height*j2) - bordivert*j2-bordiestremi) - 30

    bordifinali=0

    x = 0
    y = 0

    #DISTRIBUZIONE RIGHE VUOTE
    righe_vuote = int(((j*j2)-number)/j)
    try:
        bordisupplemento = int(height/righe_vuote/j2*1.5)
    except:
        bordisupplemento = 0

    for i, film in enumerate(films):
        try:
            if i % j == 0:
                y = y + bordisupplemento
                if x != 0:
                    y = y + height + bordivert
                    x = 0
        except:
            pass

        #ULTIMA RIGA CENTRATA
        resto = number % j
        if number-i <= resto:
            bordifinali = int((j-(number % j))*length*1.15/2)

        try:
            img = Image.open(requests.get("https://a.ltrbxd.com/resized/"+film['img']+"-0-150-0-225-crop.jpg", stream=True).raw)
        except:
            img = Image.open(
                requests.get("https://s.ltrbxd.com/static/img/empty-poster-230.876e6b8e.png ", stream=True).raw)

        new = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        img = img.resize((length, height))
        img = add_corners(img, 20)
        new.paste(img, (x * (length + bordioriz) + bordiestremi + bordifinali, y + bordoalto))
        combined = Image.alpha_composite(combined, new)
        if film['like'] or film['rewatch']:
            out = Image.new("RGBA", (length, int(bordivert * 0.5)), (255, 0, 0, 0))
            if __name__ == '__main__':
                fnt = ImageFont.truetype("DejaVuSans-Bold.ttf", int(150 / j))
            else:
                fnt = ImageFont.truetype("./utils/DejaVuSans-Bold.ttf", int(150 / j))
            try:
                msg = u"\u2605" * int(int(film['rating']) / 2) + u"\u00BD" * int(int(film['rating']) % 2) + \
                      u"\u2665" * film['like'] + u"\u27F3" * film['rewatch']
            #    if film['rewatch']:
            #        msg = u"\u2605" * int(int(film['rating']) / 2) + u"\u00BD" * int(int(film['rating']) % 2) + \
            #              " " + u"\u27F3" * film['rewatch']
            #    else:
            #        msg = u"\u2605" * int(int(film['rating']) / 2) + u"\u00BD" * int(int(film['rating']) % 2) + \
            #              " " + u"\u2665" * film['like']
            except:
                msg = ""
        else:
            out = Image.new("RGBA", (length, int(bordivert*0.5)), (255, 0, 0, 0))
            if __name__ == '__main__':
                fnt = ImageFont.truetype("DejaVuSans-Bold.ttf", int(170/j))
            else:
                fnt = ImageFont.truetype("./utils/DejaVuSans-Bold.ttf", int(170 / j))
            try:
                msg = u"\u2605" * int(int(film['rating'])/2) + u"\u00BD" * int(int(film['rating']) % 2)
            except:
                msg = ""

        #w, h = fnt.getsize(msg)
        a = fnt.getbbox(msg)
        w = a[2] - a[0]
        h = a[3] - a[1]
        d = ImageDraw.Draw(out)
        d.text((int((length-w)/2), int(((bordivert*0.5)-h)/2)), msg, font=fnt, fill=(173, 255, 47))
        new.paste(out, (x * (length + bordioriz) + bordiestremi+bordifinali, height + y + bordoalto+int(bordivert*0.1)))
        combined = Image.alpha_composite(combined, new)
        x = x + 1

    out = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    if __name__ == '__main__':
        fnt = ImageFont.truetype("Moonrising.ttf", int(bordoalto * 0.5))
    else:
        fnt = ImageFont.truetype("./utils/Moonrising.ttf", int(bordoalto*0.5))
    dictmonth = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    msg = dictmonth[int(month2)] + " " + str(year2)
    #w, h = fnt.getsize(msg)
    a = fnt.getbbox(msg)
    w = a[2] - a[0]
    h = a[3] - a[1]
    d = ImageDraw.Draw(out)
    d.text((int(1080-bordiestremi-w), int(bordoalto*0.2+bordisupplemento/2)), msg, font=fnt, fill=(173, 255, 47, 255))
    combined = Image.alpha_composite(combined, out)
    #combined.show()
    rgb_im = combined.convert('RGB')
    if __name__ == '__main__':
        rgb_im.save('tmp.jpg')
        files = {'image': open('tmp.jpg', 'rb')}
    else:
        rgb_im.save('./utils/tmp.jpg')
        files = {'image': open('./utils/tmp.jpg', 'rb')}

    '''
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    '''

    return None
    urlreq = 'https://api.imgbb.com/1/upload?expiration=864000&key=d75924aaec91be8dcb79c3c5ec3547cc'

    try:
        r = requests.post(urlreq, files=files)
        print(r.text)
        jsonx = json.loads(r.text)
        return(jsonx['data']['url'].replace("\/","/"))
    except:
        return None


if __name__ == '__main__':
    print(collage('antonioorrico'))


