#!/usr/bin/env python
import os,sys,time

while True:
    time.sleep(4)
    try:
        ret = os.popen('ps -C node -o pid,cmd').readlines()
        if len(ret) < 2:
            print 'node process is down. should start it'
            time.sleep(3)
            # os.system('service apache2 restart')
    except:
        print 'Error', sys.exc_info([1])


