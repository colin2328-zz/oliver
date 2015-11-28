from bs4 import BeautifulSoup
import re


def get_contact_info(div_soup):
    name_string = div_soup.h3.a.text

    # find paragraph with contact info
    ps = div_soup.findAll('p')
    para = None
    for p in ps:
        if p.br:
            para = p
            break

    # construct address data structure
    breaks = para.findAll('br')
    address_lines = []
    for b in breaks:
        line = b.next.strip()
        if line:
            address_lines.append(line)
        if _has_zipcode(line):
            break

    first, last, creds = _get_first_last_credentials(name_string)
    phone_number = _get_phone_number(div_soup)
    address, city, state, zipcode = _get_address_city_state_zip(address_lines)

    return first, last, creds, address, city, state, zipcode, phone_number


def _get_first_last_credentials(string):
    name_credentials = string.split(',')
    credentials = name_credentials[1] if len(name_credentials) == 2 else ''
    names = name_credentials[0].split(' ')
    if len(names) == 3:
        if len(names[2]) == 1:
            last_name = names[0]
            first_name = names[1]
        elif len(names[1]) == 1:
            first_name = names[0]
            last_name = names[2]
        else:
            first_name = name_credentials[0]
            last_name = ''
    elif len(names) == 2:
        first_name = names[0]
        last_name = names[1]
    else:
        first_name = name_credentials[0]
        last_name = ''

    return first_name, last_name, credentials


def _get_address_city_state_zip(address_lines):
    city_state_zip = address_lines[-1]
    city, state_zip = [ele.strip() for ele in city_state_zip.split(',')]
    state, zipcode = state_zip.split(' ')
    address = ' '.join(address_lines[:-1])
    return address, city, state, zipcode


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
