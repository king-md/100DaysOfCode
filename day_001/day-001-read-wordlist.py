#!/usr/bin/env python3

def main():
    wordlist = set()
    wordListFilepath = "wordlist.txt"
    file_object  = open(wordListFilepath, "r")
    lasttell = -1
    currenttell = file_object.tell()
    while( currenttell > lasttell ):
        line = file_object.readline()
        lasttell = currenttell
        currenttell = file_object.tell()
        if( currenttell > lasttell ):
            wordlist.add( line )
    print( wordlist )

    return



main()

