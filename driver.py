import sys
import bijan
import kristjan
import victor

"""
Runs all test cases for a specified user
Usage: python3 driver.py [name]
"""

if __name__ == '__main__':
    try:
        ts = {'bijan', bijan, 'kristjan': kristjan, 'victor': victor}[sys.argv[1]].ts
    except KeyError:
        print('ONE.\nOF.\nUS.\nಠ‿ಠ')
        print('It would be swell if you specified bijan, kristjan, or victor.')
        print('Up to you though.')

    ts.process_data()
    ts.run_tests()
