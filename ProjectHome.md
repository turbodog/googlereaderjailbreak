Google Reader is a popular tool for reading RSS newsfeeds. In addition, it is itself a producer of RSS feeds, such as items shared by people you follow.

However, you can only access those special feeds from within Google Reader. This project is an attempt to make those feeds available for use outside of Google Reader through a command-line Python app suitable for one-off use or scheduled runs via cron.

Based partially on code and information from http://code.google.com/p/pyrfeed/, http://www.niallkennedy.com/blog/2005/12/google-reader-api.html and other places.

Usage:
```
python jbgooglereader.py [options] feedtype login password
where feedtype =
   broadcast-friends: items that your friends have shared (People You Follow)
   starred: items you have starred
   reading-list: all items in your feed, including shared items from friends
options:
   -v/--verbose: print extra information
```

An example cron line for this might be:

`28,58 * * * * python /path/to/jbgooglereader.py broadcast-friends yourgoogleaccount@gmail.com password > /path/to/googlereadershared.xml`

This will run the script twice an hour at :28 and :58 after and capture the feed XML in googlereadershared.xml. In my case, I subscribe to this file in my feedreader that runs at :00 and :30.