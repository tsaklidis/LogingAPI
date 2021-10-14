import re
import requests
import json

from bs4 import BeautifulSoup
from dateutil.parser import parse as date_parse

station = "http://penteli.meteo.gr/stations/kozani/"


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def davis_data():
    st = requests.get(station)
    soup = BeautifulSoup(st.text, 'html.parser')
    trapezi = soup.find("table")
    rows = trapezi.findChildren(['tr'])

    t = rows[3].text.replace('\n', ' ')
    temperature = float('.'.join(re.findall(r'\d+', t)))

    raw_date = rows[2].text.replace('\n', '').strip().split(',')

    h = rows[4].text.replace('\n', ' ')
    hum = float('.'.join(re.findall(r'\d+', h)))

    # Station gives time with format '3:00'
    raw_date[1] = raw_date[1].strip()

    the_date = raw_date[2]
    the_time = raw_date[1]
    date_obj = date_parse('{} {}'.format(the_date, the_time), dayfirst=True)




    return {
        'temperature': temperature,
        'humidity': hum,
        'raw_date': raw_date,
        'date': date_obj
    }
