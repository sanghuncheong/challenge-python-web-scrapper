import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency
import unicodedata

os.system("clear")

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

# print(format_currency(5000, "KRW", locale="ko_KR"))

url = "https://www.iban.com/currency-codes"
exchange_url = " https://transferwise.com/gb/currency-converter/"


def greeting():
    print("Welcome to CurreneyConvert PRO 2000\n")

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
            'country':country.capitalize(),
            'currency':currency.upper(),
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

def get_country_num(in_country_infos, purpose=""):
    if purpose == 'from':
        print("\nWhere are you from? Choose a country by number.\n")
    elif purpose == 'to':
        print("\nNow choose another country.\n")
    int_input = int(input("#: "))
    print(f"{in_country_infos[int_input]['country']}")
    return int_input

def convert_currency(in_country_infos,from_num, to_num):
    country_code_from = in_country_infos[from_num]['code']
    country_code_to = in_country_infos[to_num]['code']

    currency_from = in_country_infos[from_num]['currency']
    currency_to = in_country_infos[to_num]['currency']

    print(f"\nHow many {country_code_from} do you want to convert to {country_code_to}?")
    try:
        int_input = int(input())
        request = requests.get(f"{exchange_url}/{country_code_from}-to-{country_code_to}-rate?amount={int_input}")
        soup = BeautifulSoup(request.text, "html.parser")

        # from_amount = soup.find("input",{"id":"cc-amount-from"})['value']
        # to_amount = soup.find("input",{"id":"cc-amount-to"})['data-hj-whitelist']
        # print("from:", from_amount)
        # print("to:", to_amount)
        source = soup.find("h3",{"class":"cc__source-to-target"}).find_all("span")
        
        try:
            currency_sign_from =unicodedata.lookup(f"{currency_from} SIGN")
        except:
            currency_sign_from = country_code_from

        try:
            currency_sign_to =unicodedata.lookup(f"{currency_to} SIGN")
        except:
            currency_sign_to = country_code_to

        # print(format_currency(input, country_code_from, locale="ko_KR"))
        # print(format_currency(float(source[2].text)*int_input, country_code_from, locale="ko_KR"))

        # print(f"{format_currency(input, country_code_from, locale="ko_KR")} is {format_currency(float(source[2].text)*int_input, country_code_to, locale="ko_KR")}")
        print(f"{currency_sign_from}{int_input:,.2f} is {currency_sign_to}{(float(source[2].text)*int_input):,.2f}")
        
    except ValueError:
        print("That wasn't a number.")
        convert_currency(in_country_infos,from_num, to_num)

    # exchange_url = " https://transferwise.com/gb/currency-converter/gbp-to-usd-rate?amount=50"

def main():
    greeting()
    raw_soup = get_countrys()
    country_infos = extract_country_infos(raw_soup)
    print_country_infos(country_infos)
    
    from_num = get_country_num(country_infos, 'from')
    to_num = get_country_num(country_infos, 'to')

    convert_currency(country_infos, from_num, to_num)
main()