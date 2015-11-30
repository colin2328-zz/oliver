import argparse

from scrape import save_results
from gdoc import populate_gdoc

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get results for a city.')
    parser.add_argument('city', nargs='+', help='City to search for')
    args = parser.parse_args()
    city_name = ' '.join(args.city)
    print('Getting results for {}'.format(city_name))
    # save_results(city_name)
    print('Populating \'Provider List\' Google doc')
    num_providers = populate_gdoc()
    print('Populated document with {} providers'.format(num_providers))
