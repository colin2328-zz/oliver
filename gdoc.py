import gspread
import json
import csv
from oauth2client.client import SignedJwtAssertionCredentials


def populate_gdoc():
    json_key = json.load(open('creds.json'))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)

    gc = gspread.authorize(credentials)

    sht = gc.open('Provider List')
    worksheet = sht.get_worksheet(0)

    with open('results.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        row_count = sum(1 for row in reader)

    with open('results.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        first_new_row = worksheet.row_count + 1
        last_new_row = first_new_row + row_count
        worksheet.add_rows(row_count)
        cell_list = worksheet.range('A{}:I{}'.format(first_new_row, last_new_row - 1))

        i = 0
        for row in reader:
            first, last, creds, address, city, state, zipcode, phone = row
            row_data = [first, last, creds, '', phone, address, city, state, zipcode]
            for value in row_data:
                cell_list[i].value = value
                i += 1

    assert (i == len(cell_list))
    worksheet.update_cells(cell_list)
