#!/usr/bin/env python3

import sys
import whois



def main():

    print( len(sys.argv) )
    if( 2 == len(sys.argv) ):
        w = whois.whois( sys.argv[1] )
        print( w )

    return



main()

