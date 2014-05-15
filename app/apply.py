import app.basic
import tornado.web
from lib import applydb
from datetime import datetime
import settings
from operator import itemgetter # For post-DB call sorting


class Process(app.basic.BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #allows for admin/dev override
        submission = applydb.obtain_submission(self.current_user)
        step = self.get_argument('step', '') or str(submission["state"])
        getattr(Process, "get_step_" + step)(self, submission)

    def post(self):
        submission = applydb.obtain_submission(self.current_user)
        db_state = str(submission["state"])
        post_state = self.get_argument("state", "")
        if (db_state == post_state) :            
            getattr(Process, "post_step_" + str(submission["state"]))(self, submission)
        else :
            getattr(Process, "get_step_" + db_state)(self, submission)
            
    def get_step_0(self, submission):
        form = {"location": submission["location"], "email": submission["email"], "name": submission["name"], "web": submission["web"], "projects": submission["projects"] }
        errors = {}
        self.render('apply/step0.html', form=form, errors=errors)
    
    def get_step_1(self, submission):
        self.render('apply/step1.html', submission = submission)
        
    def get_step_2(self, submission):
        self.render('apply/step2.html', submission = submission)

    def get_step_3(self, submission):
        # Email applicant confirming completion of the application process
        try:
            submission = applydb.obtain_submission(self.current_user)
            if 'name' in submission.keys():
                name = submission['name']
            else: 
                name = submission['username']
            text = 'Thanks, %s. Your application is complete. We will begin reviewing applications shortly, and we will be in touch regarding next steps. If you have any specific questions, please reply to this email.' % submission['name']
            html = 'Thanks, %s.<br><br>Your application is complete.<br><br>We will begin reviewing applications shortly, and we will be in touch regarding next steps. If you have any specific questions, please reply to this email.' % name
            self.send_email('noreply@noreply.com', 
                            submission['email'], 
                            'Applicant Tracking Confirmation',
                            text,
                            html=html)
        except:
            print 'Error sending completed applicant an email'

        self.render('apply/confirmation.html', submission = submission)

    def post_step_0(self, submission):
        form = {
                "email": self.get_argument("email", ""),
                "name": self.get_argument("name", ""),
                "web": self.get_argument("web", ""),
                "location": self.get_argument("location", ""),
                "links": self.get_argument("links", ""),
                "projects": self.get_argument("projects", "")
        }
        errors = {}
        if not form["email"]: errors["email"] = "Email is required."
        if not form["name"]: errors["name"] = "Name is required."
        if not form["web"]: errors["web"] = "Come on, there has to be something."
        if not form["location"]: errors["location"] = "Where are you?"
        if len(errors) > 0 : 
            self.render('apply/step0.html', form=form, errors=errors)
        else :
            form["state"] = 1
            applydb.update_submission(submission, form)
            self.get_step_1(submission)
            
    def post_step_1(self, submission):
        form = {
                "novideo": self.get_argument("novideo", "0"),
                "videotoken": self.get_argument("videotoken", "")
        }
        if form["novideo"] != "1" and form["videotoken"] == "" :
            self.render('apply/step1.html', submission = submission)
        else :
            data = {
                    "video1_token": form["videotoken"],
                    "state": 2
            }
            applydb.update_submission(submission, data)
            self.get_step_2(submission)
            
    def post_step_2(self, submission):
        form = {
                "novideo": self.get_argument("novideo", "0"),
                "videotoken": self.get_argument("videotoken", "")
        }
        if form["novideo"] != "1" and form["videotoken"] == "" :
            self.render('apply/step2.html', submission = submission)
        else :
            data = {
                    "video2_token": form["videotoken"],
                    "state": 3,
                    "submitted": True,
                    "submission_date": datetime.now()
            }
            applydb.update_submission(submission, data)
            self.get_step_3(submission)
            
            
class AdminHelper(app.basic.BaseHandler):
    def has_rated_on(self, submission):
        return self.current_user in submission["ratings"]
    
    def rating_of(self, submission):
        return submission["ratings"][self.current_user]

    def nextround_rating_of(self, submission):
        if 'nextround' in submission.keys():
            if submission['nextround'] == 'true':
                return True
            else:
                return False
        else:
            return False
    
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
class AdminList(AdminHelper):
    @tornado.web.authenticated
    def get(self):
        if self.current_user not in settings.get('staff'):
            self.redirect('/')
        else:
            # Search arguments or default to all
            name = self.get_argument('name', None)
            rated_by = self.get_argument('rated_by', None)
            kwargs = {}
            
            if name:
                kwargs['name'] = {"$regex": name}
            
            if rated_by == 'unrated':
                kwargs['ratings'] = {}
            elif rated_by == 'nextround':
                kwargs['nextround'] = 'true'
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
            page_count = total_count / per_page

            if page != "all":
                page = int(page)                    
                if page <= page_count:
                    submissions = submissions[(page-1)*per_page:page*per_page]
                else:
                    page = 1

            # Override argument to show all average ratings
            show_all = self.get_argument('show_all', False)

            return self.render('apply/admin_list.html', submissions = submissions, helper = self, total_count=total_count, page_count = page_count, page = page, show_all = show_all)
    



class AdminView(AdminHelper):
    @tornado.web.authenticated
    def get(self, screen_name):
        if self.current_user not in settings.get('staff'):
            self.redirect('/')
        else:
            submission = applydb.get_submission(screen_name)
            self.render('apply/admin_view.html', submission = submission, helper = self)



class AdminApiRate(app.basic.BaseHandler):
    @tornado.web.authenticated
    def post(self, screen_name):
        if self.current_user in settings.get('staff'):
            submission = applydb.get_submission(screen_name)
            rating = self.get_argument("rating", None)
            if submission and rating != None :
                applydb.rate_submission(submission, self.current_user, float(rating))

            nextround = self.get_argument("nextround", None)
            if submission:
                submission['nextround'] = nextround
                print submission['nextround']
                applydb.update_submission(submission, {"nextround": submission['nextround']})          

