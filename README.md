Applicant Tracking
=================

Ziggeo API (http://api.ziggeo.com) allows you to integrate video recording and playback with only
two lines of code in your site, service or app. 

This is a simple applicant tracking system featuring video interviews. It was originally built by
Union Square Ventures (http://usv.com).



Technology
===========

Built with:

 * Python / [Tornado](http://tornadoweb.org)
 * [Mongodb](http://www.mongodb.com/)
 * [Twitter](http://dev.twitter.com)
 * [Sendgrid](http://sendgrid.com/docs/API_Reference/)
 * [Ziggeo](http://ziggeo.com)

Setup
======

Prior to installation, you'll need to do a few things:

* _Twitter_: Log into http://dev.twitter.com and set up a new application.  Note the "consumer key" and "consumer secret", which we'll need later on.
* Sign up for an account at http://sendgrid.com for email delivery


Configuration
-------------

General app settings are controlled via the settings.py file. You will need to provide dev/local values for the following settings:

* 'twitter_consumer_key' : '',
* 'twitter_consumer_secret' : '',
* 'sendgrid_user': '',
* 'sendgrid_secret': '',
* 'ziggeo_token': ''

Installation
------------

* start a local instance of mongo

./mongod

* OR, configure your app to use a cloud-based mongo instance, by setting "MONGODB_URL" and "DB_NAME" in settings.py

* Start the web server:

python tornado_server.py

* Site should be viewable at http://localhost:8001

