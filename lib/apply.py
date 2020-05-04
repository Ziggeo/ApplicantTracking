import tornado.web
from lib import applydb
from lib import util
from datetime import datetime
import settings
from settings import global_data
from operator import itemgetter # For post-DB call sorting


class StaffHandler(tornado.web.RequestHandler):
  def basic_auth(self, user, password):
      for admin in settings.get("admins").split(";") :
        credentials = admin.split(":")
        if (user == credentials[0] and password == credentials[1]) :
          return True
      return False

## 0 = fields, 1..len(videos) = videos, len(videos) + 1 == confirm


class Process(util.SessionHandler):
    @tornado.web.authenticated
    def get(self):
        #allows for admin/dev override
        submission = applydb.obtain_submission(self.current_user)
        step = self.get_argument('step', '') or str(submission["state"])
        if (step == "0") :
            self.get_fields(submission)
        else :
            if (int(step) > len(global_data["VIDEOS"])) :
                self.get_confirmation(submission)
            else :
                self.get_videos(submission, int(step))

    def post(self):
        submission = applydb.obtain_submission(self.current_user)
        db_state = submission["state"]
        post_state = self.get_argument("state", "")
        if (str(db_state) == post_state) :
            if (db_state == 0) :
                self.post_fields(submission)
            else :
                self.post_videos(submission, db_state)
        else :
            if (db_state == 0) :
                self.get_fields(submission)
            else :
                if (db_state > len(global_data["VIDEOS"])) :
                    self.get_confirmation(submission)
                else :
                    self.get_videos(submission, db_state)
            
    def get_fields(self, submission):
        form = {}
        for field in global_data["FIELDS"] :
            form[field["name"]] = submission[field["name"]]
        errors = {}
        self.render('apply/fields.html', form=form, errors=errors, global_data = global_data)
    
    def post_fields(self, submission):
        form = {}
        errors = {}
        tags = []
        for field in global_data["FIELDS"] :
        	if "tag" in field and field["tag"] :
        		if (self.get_argument(field["name"], "") != "") :
        			tags.append(field["tag"])
        	else :
	            form[field["name"]] = self.get_argument(field["name"], "")
	            if field["required"] and not form[field["name"]]: errors[field["name"]] = "This field is required."
        if len(errors) > 0 : 
            self.render('apply/fields.html', form=form, errors=errors, global_data = global_data)
        else :
            form["state"] = 1
            form["tags"] = tags
            applydb.update_submission(submission, form)
            self.get_videos(submission, 1)

    def get_videos(self, submission, video_index):
        global global_data
        self.render('apply/videos.html', submission = submission, global_data = global_data, video_index = video_index)
        
    def get_confirmation(self, submission):
        self.render('apply/confirmation.html', submission = submission, global_data = global_data)

            
    def post_videos(self, submission, video_index):
        form = {
                "novideo": self.get_argument("novideo", "0"),
                "videotoken": self.get_argument("videotoken", "")
        }
        if form["novideo"] != "1" and form["videotoken"] == "" and global_data['VIDEOS'][video_index - 1]["required"] :
            self.render('apply/videos.html', submission = submission, global_data = global_data, video_index = video_index)
        else :
            data = {}
            data["video" + str(video_index) + "_token"] = form["videotoken"]
            data["state"] = video_index + 1
            if (video_index == len(global_data["VIDEOS"])) :
                data["submitted"] = True
                data["submission_date"] = datetime.now()
            applydb.update_submission(submission, data)
            if (video_index + 1 > len(global_data["VIDEOS"])) :
                self.get_confirmation(submission)
            else :
                self.get_videos(submission, video_index + 1)
            
            
class AdminHelper(StaffHandler):
    def render(self, template, **kwargs):
        kwargs['current_path'] = self.request.uri
        kwargs['args_len'] = len(self.request.arguments)
        super(AdminHelper, self).render(template, **kwargs)

    def has_rated_on(self, submission):
        return self.current_user in submission["ratings"]
    
    def rating_of(self, submission):
        return submission["ratings"][self.current_user]

    def average_rating_of(self, submission):
        count = 0
        sum = 0
        for key in submission["ratings"] :
            count += 1
            sum += submission["ratings"][key]
        return sum / count if count > 0 else 0

    ''' Zander's algorithm
        Lowest rating plus 1 for every additional rating '''
    def awesome_rating_of(self, submission):
        rating_list = []
        for key in submission["ratings"] :
            rating_list.append(submission["ratings"][key])
        min_rating = min(rating_list)
        return min_rating + len(rating_list) - 1


# /apply/admin
@util.require_basic_auth
class AdminList(AdminHelper):
    def get(self):
        # Search arguments or default to all
        name = self.get_argument('name', None)
        rated_by = self.get_argument('rated_by', None)
        tags = self.get_argument('tags', None)
        kwargs = {}
        
        if name:
            kwargs['name'] = {"$regex": name, "$options": "-i"}
            
        if tags:
        	tags = tags.split()
        	tagQuery = []
        	for tag in tags:
        		tagQuery.append({"tags": {"$regex": tag, "$options": "-i"}})
        	kwargs["$and"] = tagQuery;
        
        if rated_by == 'unrated':
            kwargs['ratings'] = {}
        elif rated_by: # For rated by a specific individual
            kwargs['ratings.' + rated_by] = {"$exists": True}

        # Sort argument
        sort = self.get_argument('sort', None)
        if sort == "your_rating":
            sort = self.current_user # Hack to pass in username as part of sort

        # DB call
        submissions = applydb.get_submissions(kwargs, submitted=True, sort=sort)

        #url_base = # everything in the url except page=X

        # Sort by total rating (not in database)
        if sort == "average_rating":
            for s in submissions:
                s['average_rating'] = self.average_rating_of(s)
            submissions = sorted(submissions, key=itemgetter('average_rating'), reverse=True)

        # Sort by Zander's algorithm
        if sort == "awesome_rating":
            for s in submissions:
                s['awesome_rating'] = self.awesome_rating_of(s)
            submissions = sorted(submissions, key=itemgetter('awesome_rating'), reverse=True)


        # Pagination
        page = self.get_argument('page', '1')
        per_page = 10
        total_count = len(submissions)
        page_count = -(-total_count // per_page)

        if page != "all":
            page = int(page)                    
            if page <= page_count:
                submissions = submissions[(page-1)*per_page:page*per_page]
            else:
                page = 1

        # Override argument to show all average ratings
        show_all = self.get_argument('show_all', False)

        return self.render('apply/admin_list.html', submissions = submissions, helper = self, total_count=total_count, page_count = page_count, page = page, show_all = show_all, global_data = global_data)
    



@util.require_basic_auth
class AdminApiRate(StaffHandler):
    def post(self, screen_name):
        submission = applydb.get_submission(screen_name)
        rating = self.get_argument("rating", None)
        if submission and rating != None :
            applydb.rate_submission(submission, self.current_user, float(rating))


@util.require_basic_auth
class AdminApiComment(StaffHandler):
    def post(self, screen_name):
        submission = applydb.get_submission(screen_name)
        comment = self.get_argument("comment", None)
        if submission and comment != None :
            applydb.comment_submission(submission, self.current_user, comment)

@util.require_basic_auth
class AdminApiTags(StaffHandler):
    def post(self, screen_name):
        submission = applydb.get_submission(screen_name)
        tags = self.get_argument("tags", None)
        if submission and tags != None :
            applydb.tag_submission(submission, self.current_user, tags)
            