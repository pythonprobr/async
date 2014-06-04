"""
Wikipedia Picture of the Day (POTD) download example
"""

from __future__ import print_function

import sys
import os
import io
import re
import argparse
import datetime
import urllib2
import contextlib

POTD_BASE_URL = 'http://en.wikipedia.org/wiki/Template:POTD/'

THUMB_BASE_URL = 'http://upload.wikimedia.org/wikipedia/commons/thumb/'
THUMB_SRC_RE = re.compile(r'src=".*?/thumb/(.*?/\d+px-[^"]+)')

LOCAL_IMG_PATH = 'pictures/'

verbose = True

class ParsingException(ValueError):
    """Raised if unable to parse POTD MediaWiki source"""


def fetch_potd_url(iso_date):
    """Fetch picture name from iso_date ('YYYY-MM-DD' format)"""
    potd_url = POTD_BASE_URL + iso_date
    with contextlib.closing(urllib2.urlopen(potd_url)) as fp:
        html = fp.read()
        thumb_src = THUMB_SRC_RE.search(html)
        if not thumb_src:
            raise ParsingException('cannot find thumbnail source for ' + url)
        thumb_url = THUMB_BASE_URL+thumb_src.group(1)
    return thumb_url


def gen_month_days(year, month):
    a_date = datetime.date(year, month, 1)
    one_day = datetime.timedelta(1)
    while a_date.month == month:
        yield a_date
        a_date += one_day


def get_img_names(iso_month):
    """Fetch picture names from iso_month ('YYYY-MM' format)"""
    year, month = (int(part) for part in iso_month.split('-'))
    for day in gen_month_days(year, month):
        iso_date = '{:%Y-%m-%d}'.format(day)
        if verbose:
            print(iso_date)
        try:
            img_url = fetch_potd_url(iso_date)
        except urllib2.HTTPError:
            break
        yield (iso_date, img_url)

def get_images(iso_month, max_count=0):
    if max_count is 0:
        max_count = sys.maxsize
    img_count = 0
    total_size = 0
    for iso_date, img_url in get_img_names(iso_month):
        if verbose:
            print('\t' + img_url)
        with contextlib.closing(urllib2.urlopen(img_url)) as fp:
            img = fp.read()
        img_count += 1
        total_size += len(img)
        img_filename = iso_date + '__' + img_url.split('/')[-1]
        if verbose:
            print('\t\twriting %0.1f Kbytes' % (len(img)/1024.0))
        img_path = os.path.join(LOCAL_IMG_PATH, img_filename)
        with io.open(img_path, 'wb') as fp:
            fp.write(img)
        if img_count == max_count:
            break
    return (img_count, total_size)

def main():
    global verbose
    parser = argparse.ArgumentParser(description='Get "Pictures of The Day" from English Wikipedia for a given month')
    parser.add_argument('year_month', help='year and month in YYYY-MM format')
    parser.add_argument('-q', '--max_qty', help='maximum number of files to download', type=int)
    parser.add_argument('-v', '--verbose', help='display progress information', action='store_true')
    args = parser.parse_args()
    verbose = args.verbose
    img_count, total_size = get_images(args.year_month, args.max_qty)
    print('%s images downloaded (%0.1f Kbytes total)' %
            (img_count, total_size/1024.0))

if __name__=='__main__':
    main()
