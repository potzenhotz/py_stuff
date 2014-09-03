# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 00:53:16 2013

@author: Potzenhotz
"""

import feedparser

read = feedparser.parse('http://feeds.finance.yahoo.com/rss/2.0/headline?s=VOW3.DE&region=US&lang=en-US.rss')

print read['feed']['title']

#print read['entries'][0]['title']
#print read['entries'][0]['description']


print len(read['entries'])

#for post in d.entries:
#    print post.title + ": " + post.link + "\n"
 