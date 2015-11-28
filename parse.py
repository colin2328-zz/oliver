from bs4 import BeautifulSoup
import re


def get_contact_info(div_soup):
    name_string = div_soup.h3.a.text
    ps = div_soup.findAll('p')
    para = None
    for p in ps:
        if p.br:
            para = p
            break

    breaks = para.findAll('br')
    address_lines = []
    for b in breaks:
        line = b.next.strip()
        if line:
            address_lines.append(line)
        if _has_zipcode(line):
            break
    phone_number = _get_phone_number(div_soup)

    return name_string, address_lines, phone_number


def _get_first_last_credentials(string):
    pass


def _get_phone_number(string):
    numbers = re.findall(r'\(\d{3}\) \d{3}-\d{4}', unicode(string))
    return numbers[0] if numbers else ''


def _has_zipcode(string):
    words = string.split(' ')
    target = words[-1]
    return len(target) == 5 and target.isdigit()

text_file = open("scrape.html", "r")
html = text_file.read()
text_file.close()

soup = BeautifulSoup(html, 'html.parser')
divs = soup.findAll('div', {'class': 'col8 result group'})
for div in divs:
    print get_contact_info(div)
    # break



# First, Last, Credentials, Email, Phone number, Address, City, State, Zip
