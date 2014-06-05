
import unittest

import potd

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.html = '''<td><a href="/wiki/File:Obama_and_Biden_await_updates_on_bin_Laden.jpg" class="image" title="Situation Room"><img alt="Situation Room" src="//upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Obama_and_Biden_await_updates_on_bin_Laden.jpg/400px-Obama_and_Biden_await_updates_on_bin_Laden.jpg" width="400" height="267" srcset="//upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Obama_and_Biden_await_updates_on_bin_Laden.jpg/600px-Obama_and_Biden_await_updates_on_bin_Laden.jpg 1.5x, //upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Obama_and_Biden_await_updates_on_bin_Laden.jpg/800px-Obama_and_Biden_await_updates_on_bin_Laden.jpg 2x" data-file-width="4096" data-file-height="2731" /></a></td><td></td>'''
        pass

    def test_buid_page_url(self):
        date = '2014-05-01'
        result = potd.build_page_url(date)
        self.assertEqual(result, 'http://en.wikipedia.org/wiki/Template:POTD/2014-05-01')

    def test_potd_fetch_page_status_code(self):
        date = '2014-05-02'
        url = potd.build_page_url(date)
        response = potd.fetch_page(url)
        self.assertEqual(response.status_code, 200)

    def test_potd_extract_image_url(self):
        image_url = potd.extract_image_url(self.html)
        self.assertEqual(image_url, 'http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Obama_and_Biden_await_updates_on_bin_Laden.jpg/400px-Obama_and_Biden_await_updates_on_bin_Laden.jpg')

    def test_potd_fetch_image_jpeg(self):
        image_url = 'http://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Obama_and_Biden_await_updates_on_bin_Laden.jpg/400px-Obama_and_Biden_await_updates_on_bin_Laden.jpg'
        response = potd.fetch_page(image_url)
        self.assertEqual(response.headers['content-type'], 'image/jpeg')

    def test_potd_get_days_of_month(self):
        year = 2014
        month = 5
        days = potd.get_days_of_month(year, month)
        self.assertEqual(len(days), 31)
        self.assertEqual(1, days[0])
        self.assertEqual(31, days[-1])

    def test_potd_get_days_of_february(self):
        year = 2014
        month = 2
        days = potd.get_days_of_month(year, month)
        self.assertEqual(len(days), 28)
        self.assertEqual(1, days[0])
        self.assertEqual(28, days[-1])

    def test_potd_format_date(self):
        year = 2014
        month = 2
        day = 1
        first_date = '2014-02-01'
        date = potd.format_date(year, month, day)
        self.assertEqual(first_date, date)
        self.assertEqual(potd.format_date(2010, 11, 12), '2010-11-12')




if __name__ == '__main__':
    unittest.main()













