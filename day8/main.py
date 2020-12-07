import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import json

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")

@app.route("/")
@app.route("/?order_by")
def new_page():
  order = request.args.get('order_by', 'popular')
  print(f"GOT ORDER: {order}")
  if order == 'new':
    db_data = db.get('new')
    if db_data:
      print("FROM DB['new']")
      json_data = db_data
    else:
      print("NO DB['new'] => ", end='')
      json_data = requests.get(new).json()
      db['new'] = json_data
      print("UPDATE DB['new']")
    return render_template(
      "index.html",
      page_name = 'New',
      contents_info = json_data["hits"]
      )
  else:
    db_data = db.get('popular')
    if db_data:
      print("FROM DB['popular']")
      json_data = db_data
    else:
      print("NO DB['popular'] => ", end='')
      json_data = requests.get(popular).json()
      db['popular'] = json_data
      print("UPDATE DB['popular']")
    return render_template(
      "index.html",
      page_name = 'Popular',
      contents_info = json_data["hits"]
      )

@app.route("/<id>")
def detail_page(id):
  content = {}
  print(f"DETAIL-NUM:{id}")
  db_data = db.get(id)
  if db_data:
    print(f"FROM DB['{id}']")
    content = db_data['contnet']
    comments_info = db_data['comments_info']
    return render_template(
      "detail.html",
      content = content,
      comments_info = comments_info
    )
  else:
    print(f"NO DB['{id}'] => ", end='')
    # detail_url = make_detail_url(id[5:])
    detail_url = make_detail_url(id)
    print(f"URL: {detail_url} => ", end='')
    json_data = requests.get(detail_url).json()
    content["title"] = json_data["title"]
    content["author"] = json_data["author"]
    content["url"] = json_data["url"]
    content["point"] = json_data["points"]
    # print("\n\n", json_data)
    # print("\n\n", json_data["children"])
    for i in range(len(json_data["children"])):
      if json_data["children"][i]["author"] == None:
        # print("[deleted]")
        json_data["children"][i]["author"] = ""
        json_data["children"][i]["text"] = "[deleted]"
    db[id] = {
      'contnet': content,
      'comments_info': json_data["children"]
    }
    print(f"UPDATE DB['{id}']")
    return render_template(
      "detail.html",
      content = content,
      comments_info = json_data["children"]
    )

# @app.route("/report")
# def report():
#   word = request.args.get('word')
#   if word:
#     word = word.lower()
#     existingJobs = db.get(word)
#     if existingJobs:
#       jobs = existingJobs
#     else:
#       jobs = get_jobs(word)
#       db[word] = jobs
#   else:
#     return redirect("/")
#   return render_template(
#     "report.html", 
#     searchingBy = word,
#     resultsNumber=len(jobs),
#     jobs = jobs
#   )

# @app.route("/export")
# def export():
#   try:
#     word = request.args.get('word')
#     if not word:
#       raise Exception()
#     word = word.lower()
#     jobs = db.get(word)
#     if not jobs:
#       raise Exception()
#     save_to_file(jobs)
#     return send_file("jobs.csv")
#   except:
#     return redirect("/")

app.run(host="0.0.0.0")