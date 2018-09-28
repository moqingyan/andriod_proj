import urllib
import re
from bs4 import BeautifulSoup
import time

base = "https://f-droid.org/"

def set_soup(target_url):
    content = urllib.request.urlopen(target_url).read()
    return BeautifulSoup(content, 'html.parser')

def get_proj_github_url(proj_fd_url):
    fd_main = set_soup(proj_fd_url)
    
    git_url_block = fd_main.find("a", string = "Source Code")
    # print(git_url_block)
    if (git_url_block != None):
        git_url = git_url_block.get_attribute_list("href")[0]
    else:
        git_url = ""
        
    return git_url
    
def get_projs_urls(url):
    projs = dict()
    
    fd_index = set_soup(url)
    proj_info = fd_index.find_all(attrs = {"class":"package-header"})
    
    for proj in proj_info:
        proj_name = proj.find(attrs = {"class": "package-name"}).string
        proj_name = ''.join(proj_name.split())
        proj_f_page_url = proj.get_attribute_list("href")
        proj_github_url = get_proj_github_url(base + proj_f_page_url[0])
        projs[proj_name] = proj_github_url
    
    return projs
    
def get_url(page_number):
    if (page_number <= 0):
        return all_projs
    
    if (page_number == 1):
        page_url = base + "en/packages/"
    else:
        page_url = base + "en/packages/" + str(page_number) + '/'
    
    # give a second chance if network error
    try:
        projs = get_projs_urls(page_url)
    except urllib.error.HTTPError:
        time.sleep(10)
        projs = get_projs_urls(page_url)
    
    return projs


# all_projs = get_urls(2,2)
# print(all_projs)
