Applicant Tracking
=================

Award winning Ziggeo API (http://ziggeo.com) allows you to integrate video recording and playback with only
two lines of code in your site, service or app. 

This is a simple applicant tracking system featuring video interviews. It was originally built by
Union Square Ventures (http://usv.com).

Technology
===========

Built with:

 * Python / [Tornado](http://tornadoweb.org)
 * [MongoDB](http://www.mongodb.com/)*
 * [Ziggeo](http://ziggeo.com)
 * [Filepicker](http://filepicker.io)

* Please note that MongoDB no longer supports their extension on Heroku. For this reason you will need to do some simple steps on your own. Please read the section bellow "Setting up MongoDB" or "MongoDB migration".

Setup
======

**1. Obtain source code**
- 1.1 Clone our repository into an empty directory.
- 1.2 Delete .git directory

**2. Sign up for Heroku**

- 2.1 Go to Heroku and create an account
- 2.2 Create a Heroku application
- 2.3 Add a Credit Card
- 2.4 Add MongoLab Addon
- 2.5 Install the Heroku Toolbelt

**3. Sign up for Ziggeo**

- 3.1 Go to Ziggeo and create an account.

**4. Configure repository**

- 4.1 In your directory, start with `git init`
- 4.2 `heroku accounts:add yourappname`
- 4.3 `heroku git:remote -a yourappname`
- 4.4 `heroku accounts:set yourappname`

**5. Configure API / service keys**

- 5.1 Open settings.py in an editor
- 5.2 Change COOKIE_SECRET to something random
- 5.3 Run `heroku config` to obtain database name and URL (See Setting up MongoDB section).
- 5.4 Go to the Ziggeo application to obtain ZIGGEO_TOKEN.

**6. Customize application by editing source code.**

- 6.1 Change the title in settings.py
- 6.2 Add your administrators to settings.py
- 6.3 Update questions & videos in settings.py
- 6.4 Open the template files to change the overall look. (options)

**7. Push to production**

- 7.1 `git add .`
- 7.2 `git commit -a -m "Initial Commit"`
- 7.3 `git push heroku master`

Setting up MongoDB
===========

mLab has removed the MongoDB addon however you can still use MongoDB in your system. To set this up you have few options:
1. Use Atlas (still mLab, just different naming)
2. Use [ObjectRocket by Rackspace](https://elements.heroku.com/addons/ormongo) Heroku addon

Benefit of using ObjectRocket's addon is that it offers you to click and install the addon as you would usually using Heroku dashboard or Heroku CLI. Everything happens within Heroku and they offer support to help you with the database setup.

If you want to continue using mLab outside of scope of addon, you can do that. To do so you would need to follow these steps:

1. Go to [Atlas signup](https://www.mongodb.com/cloud/atlas/signup) page. Remember the email you use as that will be used later as your username to log in.
2. Once signed up go to [Project View](https://cloud.mongodb.com/)
3. Go through dashboard to set everything as you prefer. Please keep in mind that you need to purchase support plan in order to be able to contact their support.

To set up your Database URL please use:
`heroku config:set DB_URL={URL YOU GOT}`

You would change `{URL YOU GOT}` with the actual URL you get, so it would look something like so:
`heroku config:set DB_URI=mongodb://heroku_12345678:random_password@ds029017.mLab.com:29017/heroku_12345678`

Once you do, that is it from MongoDB side.


MongoDB migration
===========

If you were using the Applicant tracking system for a while now, then you got emails from MongoDB and Heroku about migrating your database.

Please check out the following to see how to migrate: [Guide to Migrating a Sandbox Heroku Add-on to Atlas](https://docs.mlab.com/how-to-migrate-sandbox-heroku-addons-to-atlas/)

* This could only be important to those that already had this installed. If you are new to this, you will not need to follow those steps.
* This is needed due to [Shutdown of MongoDB add-on on Heroku](https://docs.mlab.com/shutdown-of-heroku-add-on/)

Run the application locally
===========

1. Start a local instance of mongo by running `./mongod` or configure your app to use a cloud-based mongo instance, by setting "MONGODB_URL" and "DB_NAME" in settings.py

2. Start the web server `python tornado_server.py`

3. Visit application by navigating to [http://localhost:8001](http://localhost:8001)

Additional Installation Steps
===========

If you already have Python installed you are almost all set. Check out the requirements.txt for the list of modules you might need to install if they are not already installed.

You can do this by using commands like so:
```
sudo apt install python-pip
```

Followed by pip installs like so:
```
pip install tornado
pip install pymongo
pip install requests
```
Changelog
===========
Please note that we have changed "MONGODB_URI" to "DB_URI"
