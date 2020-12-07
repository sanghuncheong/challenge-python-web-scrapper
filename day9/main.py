import requests
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

app = Flask("DayEleven")


@app.route("/")
def init_page():
  print("INIT-PAGE")
  return render_template(
      "home.html",
      subreddits = subreddits,
      )

def get_agg_subreddit():
    agg_subs = []
    for subreddit in subreddits:
        if request.args.get(subreddit) == "on":
            print(f"{subreddit} : ON ",end="")
            agg_subs.append(subreddit)
    print(f"GOT:{agg_subs}")
    return agg_subs

def convert_str_to_number(x):
    key_num = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * key_num.get(x[-1].upper(), 1)
    return int(total_stars)

def get_contents(agg_subs):
    agg_contents = []
    for agg_sub in agg_subs:
        result = requests.get(f"https://www.reddit.com/r/{agg_sub}/top/?t=month", headers=headers)
        soup = BeautifulSoup(result.text, "html.parser")
        # print("soup:", soup)
        data_soup = soup.find_all("div",{"class":"_2SdHzo12ISmrC8H86TgSCp _3wqmjmv3tb_k-PROt7qFZe"})
        vote_soup = soup.find_all("div",{"class":"_1rZYMD_4xY3gRcSS3p8ODO _25IkBM0rRUqWX5ZojEMAFQ"})
        # url = soup.find_all("a",{"data-click-id":"body"})
        print("len title:", len(data_soup))
        print("len vote:", len(vote_soup))
        print("VOTE SOUP:", vote_soup)
        for i in range(len(data_soup)):
            if data_soup[i].find_parent("a")["href"][0:3] != '/r/':
                print("\n",data_soup[i].get_text(strip=True))
                print("BAD ADD")
            else:
                print("\n",data_soup[i].get_text(strip=True))
                print(data_soup[i].find_parent("a")["href"])
                print(vote_soup[i].get_text(strip=True))
                content = {
                    "subreddit":agg_sub,
                    "title":data_soup[i].get_text(strip=True),
                    "upvotes_int":convert_str_to_number(vote_soup[i].get_text(strip=True)),
                    "upvotes":vote_soup[i].get_text(strip=True),
                    "url":data_soup[i].find_parent("a")["href"],
                }
                agg_contents.append(content)
        # print(f"CONTENT: {content}")
    return agg_contents

@app.route("/read")
def read_page():
    print("READ-PAGE")
    agg_subreddits = get_agg_subreddit()
    agg_contents = get_contents(agg_subreddits)
    sorted_agg_contents = sorted(agg_contents, key=lambda k: k['upvotes_int'], reverse=True)
    return render_template(
        "read.html",
        subreddits = agg_subreddits,
        contents_info = sorted_agg_contents
    )
app.run(host="0.0.0.0")