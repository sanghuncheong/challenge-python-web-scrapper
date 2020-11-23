import os
import requests
from bs4 import BeautifulSoup

os.system("clear")
url = "https://www.iban.com/currency-codes"


def greeting():
    print("Hello! Please choose select a country by number:")

def get_countrys():
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    return soup

def extract_country_infos(in_soup):
    country_infos = []
    soup_infos = in_soup.find("table", {"class":"tablesorter"}).find("tbody").find_all("tr")
    for i in soup_infos:
        country = i.find_all("td")[0].get_text(strip=True)
        currency = i.find_all("td")[1].get_text(strip=True)
        code = i.find_all("td")[2].get_text(strip=True)
        number = i.find_all("td")[3].get_text(strip=True)
        country_infos.append({
            'country':country,
            'currency':currency,
            'code':code,
            'number':number            
        })
    return country_infos

def print_country_infos(in_country_infos):
    for i in range(len(in_country_infos)):
        print(f"# {i} {in_country_infos[i]['country']}")

def get_country_num(num_max):
    raw_input = input("#: ")
    try:
        int_input = int(raw_input)
        if int_input < num_max:
            return int_input
        else:
            print("Choose a number from the list.")
            return -1
    except:
        print("That wasn't a number.")
        return -1
    

def print_chosen_num(in_country_infos, in_num):
    print(f"You chose {in_country_infos[in_num]['country']}\nThe currency code is {in_country_infos[in_num]['currency']}")

def main():
    greeting()
    raw_soup = get_countrys()
    country_infos = extract_country_infos(raw_soup)
    print_country_infos(country_infos)
    while 1:
        chosen_country_num = get_country_num(num_max=len(country_infos))
        if chosen_country_num != -1:
            break;
    print_chosen_num(country_infos, chosen_country_num)
    
main()