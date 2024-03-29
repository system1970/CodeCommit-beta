import requests
import datetime
from pytz import timezone
from tzlocal import get_localzone
from github import Github
import os
import base64
import json
import pyrebase
from git import Repo
from Repository import repo_name
from bs4 import BeautifulSoup as bs4


TASKS = [""]
CURRENT_TASK = []
def create_repo():
    repo_name = input("Enter repo name: ")
    try:
        g = Github("a725b3cb66377aea2e2233e9f299b31362784310")  # safer alternative, if you have an access token
        u = g.get_user()
        repo = u.create_repo(repo_name)
    except:
        pass

    sha_link = requests.get("https://api.github.com/repos/system1970/"+str(repo_name)+"/contents/README.md")
    try:    
        sha = sha_link.json()['sha']
        readme_text = "# CodeForces Solutions\nThis web service lets you have github page updated with all the the correct submissions\n you submit on codeforces.(!This only works for the solutions you submit on codeforces not any other site)\n You github page is updated with the solns you submit every day(!every day not every 24).\n If you have not submitted any it will not push anything onto github.\nYou can the info we ask for without any fear as we encode all our users info such as your gmail,passwords&github token.\nReport Bugs at pracursergamedev@gmail.com or prabhakaran.code@gmail.com, the second mail is recommended as I use it more often"
        urlSafeEncodedBytes = base64.urlsafe_b64encode(readme_text.encode("utf-8"))
        urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")
        payload = {"message": "created readme.md file in the repo",
                "author": {"name": "system1970","email": "prabhakaran.code@gmail.com"},
                "content": urlSafeEncodedStr,
                "sha": sha}
        readme = requests.put("https://api.github.com/repos/system1970/"+str(repo_name)+"/contents/README.md", 
                            auth=("system1970", "a725b3cb66377aea2e2233e9f299b31362784310"), 
                            json=payload)
    except:
        try:
            readme_text = "# CodeForces Solutions\nThis web service lets you have github page updated with all the the correct submissions\n you submit on codeforces.(!This only works for the solutions you submit on codeforces not any other site)\n You github page is updated with the solns you submit every day(!every day not every 24).\n If you have not submitted any it will not push anything onto github.\nYou can the info we ask for without any fear as we encode all our users info such as your gmail,passwords&github token.\nReport Bugs at pracursergamedev@gmail.com or prabhakaran.code@gmail.com, the second mail is recommended as I use it more often"
            urlSafeEncodedBytes = base64.urlsafe_b64encode(readme_text.encode("utf-8"))
            urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")
            payload = {"message": "created readme.md file in the repo",
                    "author": {"name": "system1970","email": "prabhakaran.code@gmail.com"},
                    "content": urlSafeEncodedStr}
            readme = requests.put("https://api.github.com/repos/system1970/"+str(repo_name)+"/contents/README.md", 
                                auth=("system1970", "a725b3cb66377aea2e2233e9f299b31362784310"), 
                                json=payload)
        except:
            pass
def Add_To_Database(data):
    db.child("userInfo").child("OwnKey").set(data)

def User_Creation():
    user = auth.create_user_with_email_and_password(email,password)
#User authentication
config = {
  "apiKey": "AIzaSyDDiXvLTuO_ECz0WOUol-9ErxeKOkD3A3E",
  "authDomain": "codeforces-ee268.firebaseapp.com",
  "databaseURL": "https://codeforces-ee268.firebaseio.com",
  "projectId": "codeforces-ee268",
  "storageBucket": "codeforces-ee268.appspot.com",
  "messagingSenderId": "1032774108703",
  "appId": "1:1032774108703:web:5d3658fa94d3270022f72a",
  "measurementId": "G-EF718751VF"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
email = input('Email: ')
password = input('Password: ')
# try:
#     User_Creation()
# except:
#     user = auth.sign_in_with_email_and_password(email,password)
try:
    user = auth.sign_in_with_email_and_password(email,password)
except:
    user = auth.create_user_with_email_and_password(email,password)
# user = auth.sign_in_with_email_and_password(email,password)
print(user)

    # getting submissions
r = requests.get("https://codeforces.com/api/user.status?handle=pracurser&from=1&count=50")
json_format_before = r.json()
json_format = []

# current day submissions
for i in range(50):
    timestamp = json_format_before["result"][i]["creationTimeSeconds"]
    value = datetime.datetime.fromtimestamp(timestamp)
    # timezone correction -> {
    format = "%d"
    # Current time in UTC
    UTC = datetime.datetime.now(timezone('UTC'))
    # Convert to local time zone
    local = UTC.astimezone(get_localzone())
                                                    # TODO: 1)convert now() to current timezone (100% completeT)
                                                    #       2)change it to be user input 
    if (datetime.datetime.now().day==value.day):    
        json_format.append(json_format_before["result"][i])
    else:
        break
    # } <-
print()

# no submission for the day
if len(json_format)==0:
    exit

problems = {}
for i in range(len(json_format)):
    problem_name = json_format[i]["problem"]["name"]
    if json_format[i]["verdict"]=="OK" and problem_name not in problems:
        problem_type = json_format[i]["problem"]["index"]
        submission_id = json_format[i]["id"]
        contest_id = json_format[i]["contestId"]
        problems[problem_name] = True

        # get problem url and name
        prblm_url = "https://codeforces.com/problemset/problem/"
        prblm_link = "# "+prblm_url+str(contest_id)+'/'+str(problem_type)
        prblm_name = "# "+str(problem_name)

        # scrape solution
        contest_url = "https://codeforces.com/contest/"
        submission = requests.get(contest_url+str(contest_id)+"/submission/"+str(submission_id))
        soup = bs4(submission.content,features="html.parser")
        soln_code = soup.findAll("pre", attrs={"id": "program-source-text"})
        code_prefix = '[<pre class="prettyprint lang-py linenums program-source" id="program-source-text" style="padding: 0.5em;">' # TODO: generalize for lang
        add_prblm_link = str(soln_code).replace(code_prefix,prblm_link+"\n"+prblm_name+"\n\n")
        solution = str(add_prblm_link).replace("</pre>]","") 

        # write to file #TODO: remove the writable file (100% complete)
        # directly create the file in github with it's api->{
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, "./Codeforces/"+str(problem_type)+"/"+str(problem_name)+".py") # TODO: generalize for lang
        f = open(file_path, "w") 
        f.write(solution) 
        f.close() 
        # }<-

        #Attempts to replace:
        #Attempt - 1 (FAIL)
        # create_repo = requests.put("https://api.github.com/repos/system1970/CodeForces/contents/README.md")
        # print(create_repo.json())
        #Attempt - 2 (SUCCESS)
        # Update README.md
        # TODO: Remove the below line
        file_text = solution
        sha_link = requests.get("https://api.github.com/repos/system1970/"+str(repo_name)+"/contents/"+str(problem_type)+"/"+str(problem_name)+".py")
        gitToken = input("ENTER YOUR GET PERSONAL TOKEN: ")
        data = {"gitToken":gitToken}
        db.child("userInfo").child("OwnKey")
        userToken = db.child("userInfo").child("OwnKey").val()
        print(userToken)
        try:    
            sha = sha_link.json()['sha']
            urlSafeEncodedBytes = base64.urlsafe_b64encode(file_text.encode("utf-8"))
            urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")
            payload = {"message": "added solutions to repo",
                    "author": {"name": "system1970","email": "prabhakaran.code@gmail.com"},
                    "content": urlSafeEncodedStr,
                    "sha": sha}
            readme = requests.put("https://api.github.com/repos/system1970/"+str(repo_name)+"/contents/"+str(problem_type)+"/"+str(problem_name)+".py", 
                                auth=("system1970", "a725b3cb66377aea2e2233e9f299b31362784310"), 
                                json=payload)
        except:
            urlSafeEncodedBytes = base64.urlsafe_b64encode(file_text.encode("utf-8"))
            urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")
            payload = {"message": "added solutions to repo",
                    "author": {"name": "system1970","email": "prabhakaran.code@gmail.com"},
                    "content": urlSafeEncodedStr}
            readme = requests.put("https://api.github.com/repos/system1970/"+str(repo_name)+"/contents/"+str(problem_type)+"/"+str(problem_name)+".py", 
                                auth=("system1970", "a725b3cb66377aea2e2233e9f299b31362784310"), 
                                json=payload)

        # TODO: remove this when finished its not part of the project->{
        PATH_OF_GIT_REPO = "D:\CodingStuff\ZCodeforcesProject\CodeForces-1\.git"  # make sure .git folder is properly configured
        COMMIT_MESSAGE = 'Solutions have been added'
        # # } <I_I>-->(BAD)

        # Push to github
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
        # Use github api to push files

# TODO: push to github(os indep.) 100%-complete...

# watch system design yt vids ... gaurav sen, tushor roy

# TODO: WebService-fy -> flask/django (IN PROGRESS)
# TODO: explore hosting options[db-firebase]
    # subscribe:
    # -> auth - gmail
    # -> profile - github token - codeforces handle
    # TODO: schedule


# TODO: refactoring
