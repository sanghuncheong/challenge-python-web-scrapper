# import url
import requests
from bs4 import BeautifulSoup

def get_jobs(word):
  url = f"https://stackoverflow.com/jobs?q={word}&r=true"
  last_page = get_last_page(url)
  print(f"last-page:{last_page}")
  jobs = extract_jobs(last_page, url, word)
  print(f"len jobs: {len(jobs)}")
  return jobs

def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  try:
    pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    print(f"LAST PAGE : {last_page}")
    return int(last_page)
  except:
    print(f"LAST PAGE = FIRST PAGE")
    last_page = 1
    return last_page
  # return 8

def extract_job(html):
  title = html.find("div", {"class":"grid--cell fl1"}).find("h2").find("a")["title"]
  # print(title)
  company, location = html.find("div", {"class":"grid--cell fl1"}).find("h3").find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  job_id = html['data-jobid']
  return {
    'title':title, 
    'company':company, 
    'apply_link':f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page, url, word):
  jobs = []
  print(f"\nScrapping Stackoverflow with the word: {word}")
  print(f"SO URL:{url}")
  try:
    for page in range (last_page):
      # print("page", page + 1)
      result = requests.get(f"{url}&pg={page + 1}")
      soup = BeautifulSoup(result.text, "html.parser")
      
      results = soup.find_all("div", {"class":"-job"})
      for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs
  except:
    print("NO JOBS ON stackoverflow")
    return jobs

  # pages = soup.find("div", {"class":"s-pagination"})
  # # pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
  # print(pages)
  
  # last_page = pages[-2]
  # last_page = pages[-2].get_text(strip=True)
  # print(last_page)
  

