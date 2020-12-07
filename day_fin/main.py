"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

# in csv, we need [title, company, link]

import requests
from flask import Flask, render_template, request, redirect, send_file
from scrapper_so import get_jobs as get_so_jobs
from scrapper_ww import get_jobs as get_ww_jobs
from scrapper_rm import get_jobs as get_rm_jobs

from exporter import save_to_file

from bs4 import BeautifulSoup
import json

url_so = "https://stackoverflow.com/jobs?r=true&q=python"
url_ww = "https://weworkremotely.com/remote-jobs/search?term=python"
url_rm = "https://remoteok.io/remote-dev+python-jobs"


db = {}
app = Flask("DayNine")

@app.route("/")
def new_page():
    print("NEW-PAGE")
    # get_so_jobs('python')
    if db:
        db_keys = db.keys()
        db_set = []
        for db_key in db_keys:
            db_set.append({
                'key':db_key,
                'len':len(db[db_key])
            })
        return render_template(
            "home.html",
            db_set=db_set
            )
    else:
        return render_template(
            "home.html"
            )
    
@app.route("/report")
def report():
    word = request.args.get('word')
    print(f"REPORT-PAGE : {word}")
    if word:
        word = word.lower()
        existingJobs = db.get(word)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs_so = get_so_jobs(word)
            jobs_ww = get_ww_jobs(word)
            jobs_rm = get_rm_jobs(word)
            jobs = []
            jobs.extend(jobs_so)
            jobs.extend(jobs_ww)
            jobs.extend(jobs_rm)
            db[word] = jobs
    else:
        return redirect("/")
    print(f"#.of DB : {len(db)}")
    return render_template(
        "read.html", 
        searchingBy = word,
        resultsNumber=len(jobs),
        contents_info = jobs
    )


@app.route("/export")
def export():
    print("\nEXPORT START")
    try:
        word = request.args.get('word')
        print(f"EXPORT WORD: {word}")
        word = word.lower()
        jobs = db.get(word)
        save_to_file(jobs, word)
        print(f"FILE NAME : {word}.csv")
        return send_file(
            filename_or_fp=f"{word}.csv",
            mimetype='text/csv',
            as_attachment=True)
    except:
        print(f"EXPORT WORD : X")
        return redirect("/")


# @app.route("/?order_by")
# def new_page():
#   order = request.args.get('order_by', 'popular')
#   print(f"GOT ORDER: {order}")
#   if order == 'new':
#     db_data = db.get('new')
#     if db_data:
#       print("FROM DB['new']")
#       json_data = db_data
#     else:
#       print("NO DB['new'] => ", end='')
#       json_data = requests.get(new).json()
#       db['new'] = json_data
#       print("UPDATE DB['new']")
#     return render_template(
#       "index.html",
#       page_name = 'New',
#       contents_info = json_data["hits"]
#       )
#   else:
#     db_data = db.get('popular')
#     if db_data:
#       print("FROM DB['popular']")
#       json_data = db_data
#     else:
#       print("NO DB['popular'] => ", end='')
#       json_data = requests.get(popular).json()
#       db['popular'] = json_data
#       print("UPDATE DB['popular']")
#     return render_template(
#       "index.html",
#       page_name = 'Popular',
#       contents_info = json_data["hits"]
#       )

# @app.route("/<id>")
# def detail_page(id):
#   content = {}
#   print(f"DETAIL-NUM:{id}")
#   db_data = db.get(id)
#   if db_data:
#     print(f"FROM DB['{id}']")
#     content = db_data['contnet']
#     comments_info = db_data['comments_info']
#     return render_template(
#       "detail.html",
#       content = content,
#       comments_info = comments_info
#     )
#   else:
#     print(f"NO DB['{id}'] => ", end='')
#     # detail_url = make_detail_url(id[5:])
#     detail_url = make_detail_url(id)
#     print(f"URL: {detail_url} => ", end='')
#     json_data = requests.get(detail_url).json()
#     content["title"] = json_data["title"]
#     content["author"] = json_data["author"]
#     content["url"] = json_data["url"]
#     content["point"] = json_data["points"]
#     # print("\n\n", json_data)
#     # print("\n\n", json_data["children"])
#     for i in range(len(json_data["children"])):
#       if json_data["children"][i]["author"] == None:
#         # print("[deleted]")
#         json_data["children"][i]["author"] = ""
#         json_data["children"][i]["text"] = "[deleted]"
#     db[id] = {
#       'contnet': content,
#       'comments_info': json_data["children"]
#     }
#     print(f"UPDATE DB['{id}']")
#     return render_template(
#       "detail.html",
#       content = content,
#       comments_info = json_data["children"]
#     )

app.run(host="0.0.0.0")