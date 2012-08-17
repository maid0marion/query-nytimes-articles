#!/usr/bin/python
""" usage: get-nytimes-cat-stories [query] [max_pages]
	query		the query for retrieving articles
	max_pages   the maximum number of results pages
	
	License: GPL2
	Copyright (c) 2012 Julie Repass
	Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
	The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import urllib2
import simplejson
import codecs
import yaml
from optparse import OptionParser
from sys import argv

configs_file = file(os.path.join('configs', 'get-nytimes-stories.yaml'), 'r')
base_uri = "http://api.nytimes.com/svc/search/v1/article"
r_format = "json"
delim = "|"
encoding = 'utf-8'
keys = []

def main():

	""" connect to the config page, read the contents """
	configs          = yaml.load(configs_file)
	api_key = configs["api key"]
	query = configs["query"]
	max_pages = configs["max pages default"]
	fields = ','.join(configs["fields"])
	search = "?format=%s&query=%s&fields=%s" % (r_format, query, fields)
	
	""" define command line options """
	usage = "usage: %prog [options] arg1 arg2"
	parser = OptionParser()
	parser.add_option("-c", "--category", dest="des_facet_category", help="specify a descriptive facet CATEGORY for query", metavar="CATEGORY")
	parser.add_option("-m", "--max_pages", type="int", dest="max_pages", help="specify the maximum NUMBER of pages to output", metavar="NUMBER")
	(options, args) = parser.parse_args()
	if options.des_facet_category:
	    query = options.des_facet_category
	if options.max_pages:
	    max_pages = options.max_pages

	# create the output file
	fn = query.replace(':', '-').replace('[', '').replace(']', '').replace('"','').replace("'","") + '_NYT.csv'
	cat_stories = get_search_results(base_uri, search, query, max_pages, api_key) 

	# write header and rows to csv
	for i in fields.split(','):
		keys.append(i)   
	write_to_csv(fn, keys, cat_stories)

# get list of articles from search results
def get_search_results(base_uri, search, query, max_pages, api_key):
    cat_stories = []
    for i in range(max_pages):
        f = simplejson.load(urllib2.urlopen(base_uri + search + "&offset=" + str(i) + "&api-key=" + api_key))
        cats = f['results']
        if len(cats) > 0:
            for i,e in enumerate(cats):
                cat_stories.append(e)
        else:
            break
    print "Your search returned '%d' articles based on '%d' maximum results pages and the %s query parameter" % (len(cat_stories), max_pages, query)
    return cat_stories
    
def write_to_csv(fn, keys, cat_stories, delim=delim):
    mode = 'wb'
    add_header = True
    if os.path.isfile(fn):
        # make sure that we have the correct keys
        add_header = False
        mode = 'ab'
    f = codecs.open(fn, mode, encoding=encoding)
    if add_header:
        f.write(delim.join(keys) + '\n')
    for i, e in enumerate(cat_stories):
        line = []
        for k in keys:
            v = None
            if e.has_key(k): v = e[k]
            v = unicode(v)
            v = v.replace("|", "-")
            line.append(v)
        line = delim.join(line)
        if line.strip() == '': continue
        f.write(line)
        if i < len(cat_stories)-1: f.write('\n')
    f.close()
    return fn

if __name__ == '__main__':
	main()
