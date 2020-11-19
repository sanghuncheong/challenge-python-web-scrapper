import requests
import sys
import subprocess as sp

def greetings():
    print("Welcome to IsItDown.py!")
    print("Please write a URL or URLs you want to check. (separated by comma)")
    
def get_input():
    urls = []
    input_raw = input("")
    # input_raw = "aef.com, awefawef.com, https://google.com           , awjekf,"
    # print("input:", input_raw)
    input_splits = input_raw.split(',')
    for i in range(len(input_splits)):
        url_strip = input_splits[i].strip().lower()
        if url_strip != "":
            if url_strip[0:7]=='http://' or url_strip[0:8]=='https://':
                if url_strip[-4:] == '.com':            
                    urls.append(url_strip)  
                else:          
                    urls.append(url_strip) # w/o .com => not valid
            else:
                if url_strip[-4:] == '.com':    
                    urls.append('https://'+url_strip)
                else:
                    urls.append(url_strip) # w/o http and .com => not valid
        # print(i, urls) 
    # print("urls: ", urls)
    return urls


def check_valid_urls(input_urls):
    for input_url in input_urls:
        if input_url[0:7]=='http://' or input_url[0:8]=='https://':
            try:
                url_result = requests.get(input_url)
                if url_result.status_code == 200:
                    print(f"{input_url} is up!")
            except:
                if input_url[-4:0] == '.com':
                    print(f"{input_url} is down!")
                else:
                    print(f"{input_url} is not a valid URL.")  
        else:
            try:
                url_result = requests.get(input_url)
                if url_result.status_code == 200:
                    print(f"{input_url} is up!")
            except:
                print(f"{input_url} is not a valid URL.")  

def start_over():
    start_input = input("Do you want to start over? y/n ")
    if start_input == 'y':
        sp.call('clear', shell='True')
        init()
    elif start_input == 'n':
        print("k.bye")
        sys.exit()
    else:
        print("That's not a valid answer")
        start_over()

def init():
    sp.call('clear', shell='True')
    greetings()
    input_urls = get_input()
    check_valid_urls(input_urls)         
    start_over()

init()