#!/usr/bin/python
"""jbgooglereader: extract RSS feeds from Google Reader
http://allthingsrss.com
http://code.google.com/p/googlereaderjailbreak/
"""

__version__ = "0.1"
__author__ = "Lindsey Smith (lindsey@allthingsrss.com)"
__copyright__ = "(C) 2010 Lindsey Smith. GNU GPL 3."
___contributors__ = ["Lindsey Smith"]

import urllib
import urllib2
import re
import os
import getopt
import sys
urllib2.install_opener(urllib2.build_opener())

# Configurable things
useragent = 'jbgooglereader'
VERBOSE = False

# Probably non-configurable things
google_url = 'http://www.google.com'
reader_url = google_url + '/reader'
login_url = 'https://www.google.com/accounts/ClientLogin'
token_url = reader_url + '/api/0/token'
reader_url_middle = '/atom/user/-/state/com.google/'

def usage():
	print('''\
python jbgooglereader.py [options] feedtype login password
functional feedtypes:
   broadcast-friends: items that your friends have shared (People You Follow)
   starred: items you have starred
   reading-list: all items in your feed, including shared items from friends
options:
   -v/--verbose: print extra information (requires feedparser.py)''')

def get_SID(login, password):
    header = {'User-agent' : useragent}
    post_data = urllib.urlencode({ 'Email': login, 'Passwd': password, 'service': 'reader', 'source': useragent, 'continue': google_url, })
    request = urllib2.Request(login_url, post_data, header)
	
    try :
        f = urllib2.urlopen( request )
        result = f.read()
    except:
        print('Error logging in as with username %s' % login)
        return None
        
    return re.search('SID=(\S*)', result).group(1)

def get_results(SID, url):
    header = {'User-agent' : useragent}
    header['Cookie']='Name=SID;SID=%s;Domain=.google.com;Path=/;Expires=160000000000' % SID

    request = urllib2.Request(url, None, header)
    
    try :
        f = urllib2.urlopen( request )
        result = f.read()
    except:
        print('Error getting data from %s' % url)
    
    return result

if __name__ == '__main__':
	try:
		opts, args = getopt.getopt(sys.argv[1:], "v", ["verbose"])
	except getopt.GetoptError as err:
		usage()
		sys.exit(-1)
	for o, a in opts:
		if o in ('-v', '--verbose'):
			VERBOSE = True
			
	if len(args) != 3:
		usage()
		sys.exit(-1)
	feedname = args[0]
	login = args[1]
	password = args[2]

	SID = get_SID(login, password)
	if not SID:
		sys.exit(-1)
		
	feedurl = reader_url + reader_url_middle + feedname
	feed = get_results(SID, feedurl)
	
	print(feed)

	if VERBOSE:
	   import feedparser
	   p = feedparser.parse(feed)
	   print('jbgooglereader found %d items' % len(p.entries))
