Query NYTimes Articles
======================
*Contributors:* Julie Repass (maid0marion)
*Tags:* nyt api 

Description
===========
This tool uses the New York Times (NYT) [Arcticle Search API](http://developer.nytimes.com/docs/read/article_search_api)
to query their online repository of article metadata dating from 1981 to present date.  The tool writes the metadata query output to a CSV in the same directory making it easy make an interactive viz using your platform of choice.

Setup Requirements
==================

1. You will need an API key from the New York Times.  To obtain an API key, submit a request on their [API Registration](http://developer.nytimes.com/apps/register) page.
Edit the configs/get-nytimes-stories.yaml to add your API key between the single quotes for specifying the 'api key' value.  The tool will not run without a valid API key.
NOTE: in my case the API key I received didn't work right away.  It worked fine the following day.
2. [simplejson](https://github.com/simplejson/simplejson) library installed for python. To install, download the library and install using "setup.py install" and any relevant options.
3. [pyyaml](https://github.com/yaml/pyyaml) library installed for python, just like for simplejson.

Configuring Defaults
====================
The configuration settings are specified in configs/get-nytimes-stories.yaml.

Defining a Query
----------------
In the configuration file the default query is set to 'des_facet:[CATS]' to support a test run once the API key is added.  To change the default or override the default using a
command option, you can validate the facet using the NYT's [API Request Tool](http://prototype.nytimes.com/gst/apitool/index.html).  The tool allows you to test
queries before committing them to code, which is especially useful for validating faceted queries since the tags are case-sensitive and need to be exact.  In the API tool select the Times Tags API for testing your facet queries. 
NOTE: Be aware if you are not signed in to the NYT Developer site your queries will come up empty.

Specifying Output Fields
------------------------
Current fields
* title - title of article
* url - link to full NYT story
* date - date published
* body - gives a story excerpt (found the 'abstract' field didn't yield useful results during testing)
* des_facet - descriptive facet(s) used to tag the article
* geo_facet - text location of report, varying levels of granularity (i.e., some were countries, some continents, some cities)
* nytd_geo_facet - text location of report

NOTE: Used two geo_facets in the search because they yield different results.

Specifying Maximum Pages to Output
----------------------------------
Current value = 200, but you can change the default maximum number of results pages to write here or override the default in an optional commandline argument.

Commandline Options
===================
When running the tool, you can specify two options to override the defaults:
1. -q argv where argv=des_facet:[NEW_CATEGORY_QUERY]
2. -m argv where argv=MAX # pages to output




