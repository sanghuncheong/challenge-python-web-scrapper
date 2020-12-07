import requests
from flask import Flask, render_template, request

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
@app.route("/order_by=popular")
def home():
  return render_template("index.html")

@app.route("/order_by=new")
def new_page():
    return render_template("detail.html")

@app.route("/hehehe")
def hellp():
    return render_template("detail.html")

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