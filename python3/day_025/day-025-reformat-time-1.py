#!/usr/bin/env python3

import argparse
import re
from dateutil import parser
from datetime import datetime
from datetime import timezone



def main():
        # get command line parameters

    # prefix_chars is used to change the option prefix characters.
    myargparser = argparse.ArgumentParser( prefix_chars='-+/' )

    # --help
    myargparser.add_argument('-help', '/?', '/help', '-usage', '--usage', '/usage',
                        action='help',
                        help='show this help message and exit')

    # --version
    myargparser.add_argument('-V', '-version', '--version', '/version',
                        action='version',
                        version='%(prog)s 1.0')

    #======================================================================
    #======================================================================
    # time
    myargparser.add_argument('-t', '--time',
                        action='store',
                        dest='timestring',
                        default=False,
                        help=' time <time string> - the time value to be reformatted')

    # format
    myargparser.add_argument('--format',
                        action='store',
                        dest='formatstring',
                        default=False,
                        help=' formatstring <time format> - the time for the outputted format')

    results = myargparser.parse_args()
    print(results)
    print(results.timestring)
    # datetime_object = datetime.strptime(results.timestring)
    theTime = parser.parse(results.timestring)
    print(theTime)
    print( "EPOCH for theTime of Sun, 25 Feb 2018 15:53:51 -0800 (PST):", theTime.timestamp())
    #print(datetime.datetime(1970,1,1).timestamp())
    print( "EPOCH0: ", datetime(1970,1,1,0,0,0,0,timezone.utc).timestamp() )
    #print( (theTime - datetime.datetime(1970,1,1)).total_seconds() )
        #(datetime.datetime(2012,04,01,0,0) - datetime.datetime(1970,1,1)).total_seconds()
    print(results.formatstring)

    return 0


if( "__main__" == __name__ ):
    # execute only if run as a script
    main()
