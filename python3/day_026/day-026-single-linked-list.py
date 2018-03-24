#!/usr/bin/env python3

import argparse
#import re
#from dateutil import parser
#from datetime import datetime
#from datetime import timezone
import random



class Node(object):

    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_next(self, new_next):
        self.next_node = new_next



class LinkedList(object):
    def __init__(self, head=None):
        self.head = head

    def insert(self, data):
        new_node = Node(data)
        new_node.set_next(self.head)
        self.head = new_node

    def size(self):
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.get_next()
        return count

    def search(self, data):
        current = self.head
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                current = current.get_next()
        if current is None:
            raise ValueError("Data not in list")
        return current

    def delete(self, data):
        current = self.head
        previous = None
        found = False
        while current and found is False:
            if current.get_data() == data:
                found = True
            else:
                previous = current
                current = current.get_next()
        if current is None:
            raise ValueError("Data not in list")
        if previous is None:
            self.head = current.get_next()
        else:
            previous.set_next(current.get_next())



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
    myargparser.add_argument('-n', '--number',
                        action='store',
                        dest='number_rand_values',
                        default="0",
                        help=' number <count> - the number of random values to insert into a linked list.')

    # format
    myargparser.add_argument('--values',
                        action='store',
                        dest='value_list_str',
                        default="",
                        help=' values <list of values> - the list of values to insert into a linked list.')

    results = myargparser.parse_args()
    print(results)
    print("Number: "+results.number_rand_values)
    print("Values: "+results.value_list_str)

    ll = LinkedList()
    if(int(results.number_rand_values) > 0):
        for i in range(int(results.number_rand_values)):
            print( "  element:", i)
            ll.insert( random.random() )

    if( len(results.value_list_str) > 0 ):
        for i in results.value_list_str.split(','):
            print( "  ELEMENT:", i)
            ll.insert( i )

    print( ll )
    print( ll.head )
    print( ll.head.data )
    print( ll.head.next_node )
    print( ll.head.next_node.data )
    print( ll.head.next_node.next_node )
    print( ll.head.next_node.next_node.data )
    return 0


if( "__main__" == __name__ ):
    # execute only if run as a script
    main()
