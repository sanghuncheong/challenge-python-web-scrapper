import os
import csv
import requests
from bs4 import BeautifulSoup
from alba import get_jobs as get_alba_jobs
from save import save_to_file


os.system("clear")
alba_url = "http://www.alba.co.kr"

if __name__ == "__main__":
    print("main start")
    alba_jobs = get_alba_jobs()