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
 * [Ziggeo](http://ziggeo.com)

Setup
======

1 Obtain our code
1.1 Clone our repository into an empty directory.
1.2 Delete .git directory
2 Obtain Heroku
2.1 Go to Heroku and create an account
2.2 Create a Heroku application
2.3 Add a Credit Card
2.4 Add MongoLab Addon
2.5 Install the Heroku Toolbelt
3 Obtain Ziggeo
3.1 Go to Ziggeo and create an account.
4 Configure Repository
4.1 In your directory, start with git init
4.2 heroku accounts:add yourappname --auto
4.3 heroku git:remote -a yourappname --account yourappname
4.4 heroku accounts:set yourappname
5 Configure Keys
5.1 Open settings.py in an editor
5.2 Change COOKIE_SECRET to something random
5.3 Run heroku config to obtain DB_NAME, MONGODB_URL.
5.4 Go to the Ziggeo application to obtain ZIGGEO_TOKEN.
6 Customize Application by changing the source code.
6.1 Change the title in settings.py
6.2 Add your administrators to settings.py
6.3 Open the template files to change the overall look and the questions.
7 Push to production
7.1 git add .
7.2 git commit -a -m "Initial Commit"
7.3 git push heroku master



Installation
------------

* start a local instance of mongo

./mongod

* OR, configure your app to use a cloud-based mongo instance, by setting "MONGODB_URL" and "DB_NAME" in settings.py

* Start the web server:

python tornado_server.py

* Site should be viewable at http://localhost:8001

