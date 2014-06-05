import calendar
import datetime
import re
import requests

def build_page_url(date):
    base_url = 'http://en.wikipedia.org/wiki/Template:POTD/'
    return base_url + date

def fetch_page(url):
    response = requests.get(url)
    return response

def extract_image_url(html):
    re_image = r'src="(//upload\..*?)"'
    image_url = re.search(re_image, html)
    return 'http:' + image_url.group(1)

def get_days_of_month(year, month):
    lastday = calendar.monthrange(year, month)[1]
    days = [x for x in range(1, lastday + 1)]
    return days

def format_date(year, month, day):
    return '{year}-{month:02d}-{day:02d}'.format(**locals())

# def get_iso_dates(year, month):
#     days = get_days_of_month(year, month)

