import os
import csv
import requests
from bs4 import BeautifulSoup
from save import save_to_file

alba_url = "http://www.alba.co.kr"

def get_super_brand_companies():
    company_infos = []
    result = requests.get(alba_url)
    soup = BeautifulSoup(result.text, "html.parser")
    companies = soup.find("div", {"id":"MainSuperBrand"}).find_all("a",{"class":"goodsBox-info"})
    # print("\ncompanies:", companies[0])
    print(companies[0]["href"])
    print(companies[0].find("span", {"class":"company"}).get_text(strip=True))
    # print("\ncompanies:", companies[1])
    for company in companies:
        company_infos.append(
            {"name" : company.find("span", {"class":"company"}).get_text(strip=True),
            "link":company["href"]}
            )
    print(company_infos[0])
    print(company_infos[1])
    return company_infos

def get_last_page(link):
    result = requests.get(f"{link}")
    soup = BeautifulSoup(result.text, "html.parser")
    try:
        tot_job_num = soup.find("p", {"class":"jobCount"}).get_text(strip=True)
        print(tot_job_num, tot_job_num[:-1])
        last_page = int(int(tot_job_num[:-1].replace(',','')) / 50) + 1
        # print("last_page", last_page)
        return last_page
    except:
        tot_job_num = soup.find("p", {"class":"listCount"}).get_text(strip=True)
        print(tot_job_num, tot_job_num[1:-1])
        last_page = int(int(tot_job_num[1:-1].replace(',','')) / 50) + 1
        # print("last_page", last_page)
        return last_page


def extract_jobs(company_name, link):
    job_infos = []
    print(f"\nTry: {company_name} {link}")
    last_page =get_last_page(link)
    print("last_page", last_page)
    for page in range(last_page):
        result = requests.get(f"{link}/job/brand/?page={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        titles = soup.find_all("td",{"class":"local"})
        companies = soup.find_all("span", {"class":"company"})
        time = soup.find_all("td", {"class":"data"})
        pay = soup.find_all("td", {"class":"pay"})
        reg_time = soup.find_all("td", {"class":"regDate"})
        for i in range(len(titles)):
            job_infos.append(
                {
                    "place":titles[i].get_text(strip=True),
                    "title":companies[i].get_text(strip=True),
                    "time":time[i].get_text(strip=True),
                    "pay":pay[i].get_text(strip=True),
                    "date":reg_time[i].get_text(strip=True)
                }
            )
    return job_infos

def get_jobs():
    company_infos = get_super_brand_companies()
    for company in company_infos:
        job_infos = extract_jobs(company["name"], company["link"])
        print("total jobs:", len(job_infos))
        save_to_file(company["name"], job_infos)
    
    
    return 1

# def get_jobs():
#   last_page = get_last_page()
#   jobs = extract_jobs(last_page)
#   return jobs
  
# def get_last_page():
#   result = requests.get(URL)
#   soup = BeautifulSoup(result.text, "html.parser")
#   pagination = soup.find("div", {"class":"pagination"})
#   links = pagination.find_all('a')
#   pages = []
#   for link in links[:-1]:
#     pages.append(int(link.string))
#   max_page = pages[-1]
#   return max_page

# def extract_job(html):
#   title = html.find("h2", {"class":"title"}).find("a")["title"]
#   company = html.find("span", {"class": "company"})
#   company_anchor = company.find("a")
#   if company_anchor is not None:
#     company = str(company_anchor.string)
#   else:
#     company = str(company.string)
#   company = company.strip()
#   # print(title, company)
#   location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
#   # print(location)
#   job_id = html["data-jk"]
#   # print(job_id)
#   return {'title': title, 'company': company, 'location': location, "link":f"https://www.indeed.com/viewjob?jk={job_id}"}

# def extract_jobs(last_page):
#   jobs = []
#   for page in range(last_page):
#     print(f"Scrapping Indeed page {page}")
#     result = requests.get(f"{URL}&start={page*LIMIT}")
#     # print(result.status_code) # just checking if the page is working
#     soup = BeautifulSoup(result.text, "html.parser")
#     results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
#     # print("results:", results)
#     for result in results:
#       # print("\n\n\n", result)
#       job = extract_job(result)
#       jobs.append(job)
#   return jobs
