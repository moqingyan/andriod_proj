import get_fdriod_urls as gfu
import github_info as gi
import json
import os


data_path = os.path.abspath(os.path.join('../', 'data'))
android_repo_path = os.path.join (data_path, 'andriod_repos.json')
android_repo_file = open(android_repo_path, 'a+')

start_page_number = 10
end_page_number = 20


#every line is a json object corresponds to projs in a page
for pg in range(start_page_number, end_page_number):
    print("Working on page number: " + str(pg))
    projs_in_pg = gfu.get_url(pg)
    json.dump(projs_in_pg, android_repo_file)
    android_repo_file.write('\n')
