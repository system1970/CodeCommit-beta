import requests
import datetime
from pytz import timezone
from tzlocal import get_localzone
import os
from git import Repo
from bs4 import BeautifulSoup as bs4

# push request 
def push_Request():
    query = int(input())
    if(query)==1:
        return True
    elif(query)==0:
        return False
    else:
        push_Request()
# push to github function
def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')  

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
    print(UTC.strftime(format))
    # Convert to local time zone
    local = UTC.astimezone(get_localzone())
    if (datetime.datetime.now().day==value.day):    # TODO: convert now() to current timezone
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
        print(solution)

        # write to file
        script_dir = os.path.dirname(__file__)
        file_path = os.path.join(script_dir, "./Codeforces/"+str(problem_type)+"/"+str(problem_name)+".py") # TODO: generalize for lang
        f = open(file_path, "w") 
        f.write(solution) 
        f.close() 

        PATH_OF_GIT_REPO = "D:\CodingStuff\ZCodeforcesProject\CodeForces-1\.git"  # make sure .git folder is properly configured
        COMMIT_MESSAGE = 'Solutions have been added'

        #Push request
        if(push_Request()):
            git_push()
        


# TODO: push to github(os indep.)
# TODO: schedule
# watch system design yt vids ... gaurav sen, tushor roy

# TODO: WebService-fy -> flask/django
# TODO: explore hosting options[db-firebase]
    # subscribe:
    # -> auth - gmail
    # -> profile - github token - codeforces handle


# TODO: refactoring
