import argparse

from scrape import save_results
from gdoc import populate_gdoc

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get results for a city.')
    parser.add_argument('city', nargs='+', help='City to search for')
    parser.add_argument('--type', help='Doctor type to search for')
    args = parser.parse_args()
    city_name = ' '.join(args.city)
    doctor_type = args.type if args.type else 'lpc'
    print('Getting results for {} of type {}'.format(city_name, doctor_type))
    save_results(city_name, doctor_type)
    print('Populating \'Provider List\' Google doc')
    num_providers = populate_gdoc()
    print('Populated document with {} providers'.format(num_providers))
