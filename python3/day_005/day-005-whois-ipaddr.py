#!/usr/bin/env python3

import sys
#import dnspython
#import whois
from ipwhois import IPWhois



def main():

    print( len(sys.argv) )
    if( 2 == len(sys.argv) ):
        obj = IPWhois( sys.argv[1] )
        results = obj.lookup_rdap(depth=1)
        print( results )

    return



main()

