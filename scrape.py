import mechanize
import cookielib
import time
import sys
import os

from parse import save_results_from_page, get_number_of_pages
from user_agent import get_agent


def save_results(city_name, doctor_type):
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    # br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # Want debugging messages?
    # br.set_debug_http(True)
    # br.set_debug_redirects(True)
    # br.set_debug_responses(True)

    br.addheaders = [('User-agent', get_agent())]
    r = br.open('http://provider.bcbs.com/Search/')

    try:
        br.select_form(nr=0)
    except mechanize.FormNotFoundError:
        print('try refreshing browser- it thinks we\'re a bot')
        with open("error.html", "w") as f:
                f.write(br.response().read())
        sys.exit()

    br.form['Keyword'] = doctor_type
    br.form['Address'] = city_name
    br.form['Proximity'] = ['50']
    br.form['Product'] = ['PPO']

    br.submit()

    html = br.response().read()

    try:
        os.remove('results.csv')
    except OSError:
        pass
    try:
        os.remove('error.html')
    except OSError:
        pass

    errors = save_results_from_page(html, page_num=1)
    num_pages = get_number_of_pages(html)

    for page_num in range(2, num_pages + 1):
        time.sleep(0.5)
        url = 'http://provider.bcbs.com/ReturnToResults?PageRequested={}'.format(page_num)

        br.open(url)
        html = br.response().read()
        errors += save_results_from_page(html, page_num=page_num)

    if errors:
        print('Encountered {} errors parsing. Please check error.html'.format(errors))
