#!/usr/bin/env python3

import threading, time

def takeANap():
    time.sleep(5)
    print('Wake up!')

print('Start of program.')

threadObj = threading.Thread(target=takeANap)

threadObj.start()
print('End of program.')
