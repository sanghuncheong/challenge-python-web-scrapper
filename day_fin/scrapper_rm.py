# import url
import requests
from bs4 import BeautifulSoup

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
}

def get_jobs(word):
  url = f"https://remoteok.io/remote-dev+{word}-jobs"
  jobs = extract_jobs(url, word)
  print(f"len jobs: {len(jobs)}")
  return jobs


def extract_job(input_soup):
  return {
    'title':input_soup.find("h2").get_text(strip=True), 
    'company':input_soup.find("h3").get_text(strip=True), 
    'apply_link':f"https://remoteok.io{input_soup.find('a')['href']}"
    }


def extract_jobs(url, word):
  jobs = []
  print(f"\nScrapping Remote Software Developer with the word: {word}")
  print(f"RM URL:{url}")
  result = requests.get(url, headers=headers)
  soup = BeautifulSoup(result.text, "html.parser")
  try:
    trs = soup.find("table", {"id":"jobsboard"}).find_all("tr",{"class":"job"})
    for tr in trs:
      tds = tr.find_all("td", {"class":"company_and_position"})
      for td in tds:
        job = extract_job(td)
        jobs.append(job)
    return jobs
  except:
    print("NO JOBS ON Remote Software")
    return jobs
    # tds = tr.find_all("td", {"class":"company"}).find('a', {'class':''})

    # print(tr.find("td",{"class":"company position"}))
  # for tbody in tbodys:

  #   tds = tbody.find_all("td", {"class":"company position"})
  #   print(f"\n{tds}")
  # for result in results:
  #   job = extract_job(result)
  #   jobs.append(job)
  # return jobs

  # pages = soup.find("div", {"class":"s-pagination"})
  # # pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
  # print(pages)
  
  # last_page = pages[-2]
  # last_page = pages[-2].get_text(strip=True)
  # print(last_page)
  

