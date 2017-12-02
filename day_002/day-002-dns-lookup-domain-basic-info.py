#!/usr/bin/env python3

import sys
import socket

def main():
    print( len(sys.argv) )
    if( 2 == len(sys.argv) ):
        print( socket.gethostbyname( sys.argv[1] ) )
    else:
        print( "invalid arguments." )

    return



main()

