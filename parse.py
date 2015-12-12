from bs4 import BeautifulSoup
import re
import csv

state = set()


def _get_contact_info(div_soup):
    """First, Last, Credentials, Email, Phone number, Address, City, State, Zip"""
    name_string = div_soup.h3.a.text
    first, last, creds = _get_first_last_credentials(name_string)

    # find paragraph with contact info
    ps = div_soup.findAll('p')
    para = None
    for p in ps:
        if 'ph: (' in p.text.lower() and p.br:
            para = p
            break

    # construct address data structure
    breaks = para.findAll('br')
    address_lines = []
    address_start = False
    for b in breaks:
        line = b.previous.strip()
        if _is_address(line):
            address_start = True
        if address_start and line:
            address_lines.append(line)
        if _has_zipcode(line):
            break

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


def _add_to_set(results):
    hashed = _hash(results)
    if hashed not in state:
        state.add(hashed)


def _is_in_set(results):
    hashed = _hash(results)
    return hashed in state


def _hash(results):
    return ' '.join(sorted([results[0], results[1], results[-1]]))


def _get_phone_number(string):
    numbers = re.findall(r'\(\d{3}\) \d{3}-\d{4}', unicode(string))
    return numbers[0] if numbers else ''


def _has_zipcode(string):
    words = string.split(' ')
    target = words[-1]
    return len(target) == 5 and target.isdigit()


def _is_address(string):
    words = string
    return len(words) > 1 and words[0].isdigit()


def print_results_from_page(html, debug=False):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.findAll('div', {'class': 'col8 result group'})
    with open('results.csv', 'a') as fp:
        f = csv.writer(fp, delimiter=',')
        for div in divs:
            results = _get_contact_info(div)
            if _is_in_set(results):
                continue
            _add_to_set(results)
            if debug:
                print results
            else:
                f.writerow(list(results))


def get_number_of_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination_div = soup.find('div', {'class': 'pagination pull-right'})
    last_anchor = pagination_div.find('a', {'title': 'Load last set of results'})
    end_page = int(last_anchor.text)
    return end_page

if __name__ == '__main__':
    with open("scrape.html", "r") as f:
        html = f.read()

    print_results_from_page(html, debug=True)
