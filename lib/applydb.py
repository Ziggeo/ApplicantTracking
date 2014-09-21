from mongo import db
import pymongo
import json
import logging
from bson.objectid import ObjectId
from settings import global_data

from datetime import datetime
import requests


"""
db.apply.submissions

{
    _id: ...,
    username: String,
    creation_date: Date(),
    submission_date: Date();
    submitted: Boolean,
    state: int # 0 = nothing submitted, 1 = email, name, web, projects submitted; 2 = video 1 submitted; 3 = video 2 submitted = final state,
    email: String,
    name: String,
    comment: String,
    
    web: String,
    location: String,
    projects: String,
    
    video1_token: String, # ziggeo token
    video2_token: String, # ziggeo token
    
    ratings: Object # Associative array mapping twitter handle of admin to rating
}

"""

db.apply.submissions.ensure_index('username')
db.apply.submissions.ensure_index('submitted')
db.apply.submissions.ensure_index('submission_date')

#def get_all(include_drafts = False):
#    return list(db.apply.submissions.find()) if include_drafts else list(db.apply.submissions.find({"submitted": True}, sort=[('submission_date', pymongo.DESCENDING)])) 

def get_submission(username):
    return db.apply.submissions.find_one({"username" : username})

''' Assumes only submitted submissions are wanted '''
def get_submissions(kwargs, submitted=True, sort=None):
    if submitted and 'submitted' not in kwargs.keys():
        kwargs['submitted'] = submitted

    if sort == 'average_rating':
        sort = None # Not in database, handled in code
    elif sort: # Individual's rating
        sort = [('ratings.' + sort, pymongo.DESCENDING)]
    
    # Default to date of submission
    if not sort:
        sort = [('submission_date', pymongo.DESCENDING)]
    
    return list(db.apply.submissions.find(kwargs, sort=sort))

# Either finds the submission or creates the submission for the user
def obtain_submission(username):
    submission = get_submission(username)
    if submission :
        return submission
    submission = {
        "username": username,
        "creation_date": datetime.now(),
        "submission_date": None,
        "submitted": False,
        "state": 0,
        "comment": "",
        "ratings": {}
    }
    for field in global_data["FIELDS"]:
        submission[field['name']] = ""
    for i in range(0,len(global_data["VIDEOS"])):
        submission["video" + str(i+1) + "_token"] = None
    db.apply.submissions.insert(submission);
    return submission 

def update_submission(submission, update):
    db.apply.submissions.update({"username": submission["username"]}, {"$set": update})

def rate_submission(submission, user, rating):
    submission["ratings"][user] = rating
    update_submission(submission, {"ratings": submission["ratings"]})
