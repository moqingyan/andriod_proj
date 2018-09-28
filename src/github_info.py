import urllib
import re
from datetime import date
from bs4 import BeautifulSoup

DATEMOD_MORE_THAN_ONE = "WARNING: more than one dateModified found!"
DATETIME_MORE_THAN_ONE =  "WARNING: more than one datetime found!"


def set_soup(target_url):
    content = urllib.request.urlopen(target_url).read()
    return BeautifulSoup(content, 'html.parser')
    
def find_date_mod(soupObj):
        
    date_time = soupObj.find_all('relative-time')
    if (len(date_time) != 1):
        # print(DATETIME_MORE_THAN_ONE)
        return -1
        
    date_string = date_time[0].get('datetime')
    year = int(date_string[0:4])
    month = int(date_string[5:7])
    day = int(date_string[8:10])
    
    last_modify_date = date(year, month, day)
    today = date.today()
    no_commit_period = abs(today - last_modify_date)
    # print(no_commit_period.days)
    return no_commit_period.days
    
def find_social(soupObj):
    
    social_info = {'watch':-1, 'star':-1, 'fork':-1}
    
    # print (soupObj.encode('utf-8'))
    social_class =soupObj.find_all(attrs = {"class" : "social-count"})
    for sc in social_class:
        labels =  sc.get_attribute_list("aria-label")
        for label in labels:
            if ("watch" in label):
                social_info['watch'] = int(''.join(''.join(sc.string.split()).split(',')))
            if ("star" in label):
                social_info['star'] = int(''.join(''.join(sc.string.split()).split(',')))
            if ("fork" in label):
                social_info['fork'] = int(''.join(''.join(sc.string.split()).split(',')))
    
    #print (social_info)
    return social_info
    
def find_license(soupObj):
    return

# TODO : Need to redirect to another url
def find_issue(url):
    return

# TODO
def find_api():
    return

# TODO
def find_libraries():
    return
    

# How would I evaluate the repo?
# 1. no commit period
# 2. number of commits, watch, star, fork
# -------------------
# 3. license
# 4. number of issues and closed issues
# 5. api version
# 6. library used
class github_repo_info:
    
    def __init__(self, url):
        self.url = url
        self.author_name = url.split('/')[-2]
        self.repo_name = url.split('/')[-1]
        self.soup_main = set_soup(self.url)

        self.no_commit_period = find_date_mod(self.soup_main)
        self.social_info = find_social(self.soup_main)
    
    def to_json(self):
        git_info = dict()
        git_info['git_url'] = self.url
        git_info['author_name'] = self.author_name
        git_info['repo_name'] = self.repo_name
        git_info['no_commit_period'] = self.no_commit_period
        git_info['watch'] = self.social_info['watch']
        git_info['star'] = self.social_info['star']
        git_info['fork'] = self.social_info['fork']
        return git_info
        
    def to_string(self):
        git_info = self.to_json()
        git_res = ""
        for git_feature in git_info:
            if (git_feature != 'git_url'):
                git_res = git_res + str(git_info[git_feature]) + '\t'
        return git_res

# url = "https://github.com/vvolas/Awesome-Live-Wallpaper"
# githubinfo = github_repo_info(url)
# print (githubinfo.to_string())
