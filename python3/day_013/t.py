#!/usr/bin/env python3


def main():
    emailFilepath = "test_email_001.eml"
    file_object  = open(emailFilepath, "r")
    for line in file_object:
        print( "DEBUG:", line )
                

    return



main()

