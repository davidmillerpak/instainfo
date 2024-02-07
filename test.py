import requests
from bs4 import BeautifulSoup
import re

def find_jpg_links(html_code):
    jpg_links = re.findall(r'(https?:\\/\\/[^\s]+\.jpg(?:\?[\w=&-]*)?[^"]*)', html_code)
    return jpg_links

def getdata(user):
    url=f"https://instagram.com/{user}/"
    request= requests.get(url)
    data={}
    if request.status_code==200:
        soup=BeautifulSoup(request.text, 'html.parser')
        og_description_tag = soup.find('meta', property='og:description')
        if og_description_tag:
            og_description_tag = og_description_tag.get("content").split(", ")
            data['status']="success"
            data['info']=og_description_tag
            data['title']=soup.find("title").text.split(" (@")[0]
            jpg_links = find_jpg_links(request.text)
            if jpg_links:
                data['image']=jpg_links[0].replace("\\","")
                return data
            else:
                data['status']="error"
                return "Error: No image found"
        else:
            data['status']="error"
            return f"Error: Unable to find @{user}"
    else:
        data['status']="error"
        return f"Error {request.status_code} while fetching {url}"

uname = input("Username: ")

def process_data(mdta):
    try:
        if mdta['status'] == "success":
            info = mdta['info']
            name = mdta['title']
            dp = mdta['image'].split('":"')
            dp = dp[len(dp)-1]
            print(f"\nDP: {dp}\nName: {name}")
            for inf in info:
                print(inf.split(" - See")[0])
        else:
            print(mdta['status'])
    except KeyError as e:
        print(f"Error: Missing key {e} in response data")
    except Exception as e:
        print(f"An error occurred: {e}. Retrying...")
        mdta = getdata(uname)
        process_data(mdta)

mdta = getdata(uname)
process_data(mdta)