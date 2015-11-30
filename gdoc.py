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
        data = []
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            first, last, creds, address, city, state, zipcode, phone = row
            row_data = [first, last, creds, '', phone, address, city, state, zipcode]
            data.append(row_data)
            # worksheet.append_row()
