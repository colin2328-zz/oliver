import mechanize
import cookielib

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

user_agent = 'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)'
br.addheaders = [('User-agent', user_agent)]
r = br.open('http://provider.bcbs.com/Search/')


br.select_form(nr=0)


br.form['Keyword'] = 'lpc'
br.form['Address'] = 'San Francisco'
br.form['Proximity'] = ['50']
br.form['Product'] = ['PPO']


br.submit()

html = br.response().read()

text_file = open("scrape.html", "w")
text_file.write(html)
text_file.close()
