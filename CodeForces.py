import requests
import datetime
import os
from bs4 import BeautifulSoup
#Problem
r = requests.get("https://codeforces.com/api/user.status?handle=pracurser&from=1&count=50")
json_format_before = r.json()
json_format = []
for i in range(50):
    timestamp = json_format_before["result"][i]["creationTimeSeconds"]
    value = datetime.datetime.fromtimestamp(timestamp)
    if (datetime.datetime.now().day==value.day):
        json_format.append(json_format_before["result"][i])
    else:
        break
print()
problems = []
if len(json_format)!=0:
    for i in range(len(json_format)):
        if json_format[i]["verdict"]=="OK" and json_format[i]["problem"]["name"] not in problems:
            Id = json_format[i]["id"]
            ContestId = json_format[i]["contestId"]
            problems.append(json_format[i]["problem"]["name"])
            # Solution to Problem:
            Submission = requests.get("https://codeforces.com/contest/"+str(ContestId)+"/submission/"+str(Id))
            soup = BeautifulSoup(Submission.content,features="html.parser")
            mydivs = soup.findAll("pre", attrs={"id": "program-source-text"})
            mydivs = str(mydivs).replace('[<pre class="prettyprint lang-py linenums program-source" id="program-source-text" style="padding: 0.5em;">','https://codeforces.com/problemset/problem/'+str(ContestId)+'/'+str(json_format[i]["problem"]["index"])+"\n\n"+"              "+str(json_format[i]["problem"]["name"])+":"+"\n\n")
            Solution = str(mydivs).replace("</pre>]","")
            print(Solution)
            script_dir = os.path.dirname(__file__)
            file_path = os.path.join(script_dir, "./Codeforces/"+str(json_format[i]["problem"]["index"])+"/"+str(json_format[i]["problem"]["name"])+".txt")
            file = open(file_path, "w") 
            file.write(Solution) 
            file.close() 
            print()
