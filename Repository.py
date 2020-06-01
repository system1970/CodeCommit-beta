from github import Github
import base64
import requests
# Temporary name (for test purposes ONly!!) #TODO: Change the repo name it's just plain bad 

repo_name = input("Enter repo name: ")
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
                        auth=("system1970", "LootG0ld"), 
                        json=payload)
except:
    readme_text = "# CodeForces Solutions\nThis web service lets you have github page updated with all the the correct submissions\n you submit on codeforces.(!This only works for the solutions you submit on codeforces not any other site)\n You github page is updated with the solns you submit every day(!every day not every 24).\n If you have not submitted any it will not push anything onto github.\nYou can the info we ask for without any fear as we encode all our users info such as your gmail,passwords&github token.\nReport Bugs at pracursergamedev@gmail.com or prabhakaran.code@gmail.com, the second mail is recommended as I use it more often"
    urlSafeEncodedBytes = base64.urlsafe_b64encode(readme_text.encode("utf-8"))
    urlSafeEncodedStr = str(urlSafeEncodedBytes, "utf-8")
    payload = {"message": "created readme.md file in the repo",
            "author": {"name": "system1970","email": "prabhakaran.code@gmail.com"},
            "content": urlSafeEncodedStr}
    readme = requests.put("https://api.github.com/repos/system1970/"+str(repo_name)+"/contents/README.md", 
                        auth=("system1970", "LootG0ld"), 
                        json=payload)
# payload = {"message": "created the solutions folder",
#         "author": {"name": "system1970","email": "prabhakaran.code@gmail.com"},
#         "content": }
# readme = requests.put("https://api.github.com/repos/system1970/"+str(repo_name)+"/contents/README.md", 
#                     auth=("system1970", "LootG0ld"), 
#                     json=payload)