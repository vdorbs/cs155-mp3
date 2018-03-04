#!/usr/bin/env python3
import sys
import tests.bijan
import tests.kristjan
import tests.victor

"""
Runs all test cases for a specified user
Usage: python3 driver.py name
"""

if __name__ == '__main__':
    try:
        ts = {'bijan': tests.bijan, 'kristjan': tests.kristjan, 'victor': tests.victor}[sys.argv[1]].ts
        ts.process_data()
        ts.run_tests()
    except IndexError or KeyError:
        print('\nONE.\nOF.\nUS.\nಠ‿ಠ')
        print('It would be swell if you specified bijan, kristjan, or victor.')
        print('Up to you though.\n')
