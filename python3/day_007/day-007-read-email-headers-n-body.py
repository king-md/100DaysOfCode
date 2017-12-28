#!/usr/bin/env python3


def main():
    emailHeadersLines = []
    emailBodyLines = []
    emailFilepath = "test_email_001.eml"
    file_object  = open(emailFilepath, "r")
    #lasttell = -1
    #currenttell = file_object.tell()
    readingHeaders = True
    readingBody = False
    #while( currenttell > lasttell ):
    for line in file_object:
        #line = file_object.readline()
        #print( "DEBUG:", currenttell, lasttell, line )
        print( "DEBUG:", line )
        line = line.strip('\n')
        line = line.strip('\r')
        #lasttell = currenttell
        #currenttell = file_object.tell()
        #if( currenttell > lasttell ):
        if( 0 == len(line) ):
            readingHeaders = False
        if( True == readingHeaders ):
            emailHeadersLines.append(line)
        elif( True == readingBody ):
            emailBodyLines.append(line)
        else:
            readingBody = True
                
    print( "Emails Header Lines:", emailHeadersLines)
    print( "Emails Body Lines:", emailBodyLines)

    return



main()

