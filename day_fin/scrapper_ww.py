# import url
import requests
from bs4 import BeautifulSoup


url_ww = "https://weworkremotely.com/remote-jobs/search?term=python"


def get_jobs(word):
  url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
  jobs = extract_jobs(url, word)
  print(f"len jobs: {len(jobs)}")
  return jobs

def extract_job(input_soup):
  if len(input_soup.find_all('a')) > 1:
    try:
      return {
      'apply_link': f"https://weworkremotely.com{input_soup.find_all('a')[1]['href']}",
      'company' : input_soup.find_all('a')[1].find("span",{"class":"company"}).get_text(strip=True),
      'title': input_soup.find_all('a')[1].find("span",{"class":"title"}).get_text(strip=True)
      }
    except:
      return None
  else:
    try:
      return {
      'apply_link': f"https://weworkremotely.com{input_soup.find_all('a')[0]['href']}",
      'company' : input_soup.find_all('a')[0].find("span",{"class":"company"}).get_text(strip=True),
      'title': input_soup.find_all('a')[0].find("span",{"class":"title"}).get_text(strip=True)
      }
    except:
      return None

def extract_jobs(url, word):
  jobs = []
  # print("page", page + 1)
  print(f"\nScrapping weworkremotely with the word: {word}")
  print(f"WW URL:{url}")
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  try:
    sections = soup.find_all("section",{"class":"jobs"})
    for section in sections:
      lis = section.find("article").find("ul").find_all("li")
      for li in lis[:-1]:
        job = extract_job(li)
        # print(job)
        if job:
          jobs.append(job)
    # print(jobs[0:3])
    return jobs
  except:
    print("NO JOBS ON weworkremotely")
    return jobs

  # pages = soup.find("div", {"class":"s-pagination"})
  # # pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
  # print(pages)
  
  # last_page = pages[-2]
  # last_page = pages[-2].get_text(strip=True)
  # print(last_page)
  

