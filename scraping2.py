import json
import requests
import time
import math
import csv
import random
from bs4 import BeautifulSoup

#Peter Reid

#TO DO: Make functions for gathering single page of data and for extracting values from data
#TO DO: Write to a csv to store results

url = "https://www.zillow.com/princeton-nj/sold/"
page_number = 1
footer = "_p/"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

soup = BeautifulSoup(requests.get(url+str(page_number)+footer, headers=headers).content, "html.parser")
results=soup.find("span", class_="result-count").text.split()[0].replace(",","")
print(results)
data = json.loads(
    soup.select_one("script[data-zrr-shared-data-key]")
    .contents[0]
    .strip("!<>-")
)
print(data['cat1'].keys())
#print(data.keys())
print(data['cat1']['searchResults']['listResults'][0].keys())
print(data['cat1']['searchResults']['listResults'][0]['variableData'].keys())
print(data['cat1']['searchResults']['listResults'][0]['hdpData']['homeInfo'].keys())
all_data = data['cat1']['searchResults']['listResults']
num_pages = math.ceil(int(results)/40)
print(num_pages)

# print(json.dumps(data, indent=4))
# print(all_data[0].keys())
count=0
houses = []
for i in range(len(all_data)):
    print(i)
    try:
        price = all_data[i]['units'][0]['price']
    except KeyError:
        price = all_data[i]['unformattedPrice']
    try:
        assessment = all_data[i]['hdpData']['homeInfo']['taxAssessedValue']
    except KeyError:
        assessment = "Missing"
    try:
        zest = all_data[i]['hdpData']['homeInfo']['zestimate']
    except KeyError:
        zest = "Missing"
    try:
        sold_date = all_data[i]['hdpData']['homeInfo']['dateSold']
    except KeyError:
        sold_date = "Missing"
    try:
        status = all_data[i]['hdpData']['homeInfo']['homeStatus']
    except KeyError:
        status = "Missing"
    hometype = all_data[i]['hdpData']['homeInfo']['homeType']
    address = all_data[i]['address']
    area = all_data[i]['area']
    beds = all_data[i]['beds']
    baths = all_data[i]['baths']

    link = all_data[i]['detailUrl']
    # sometimes the link does not contain the starting website url, thats why we are inserting "https://www.zillow.com{link}" at the starting of link
    if 'http' not in link:
        link_to_buy = "https://www.zillow.com" + link
    else:
        link_to_buy = link
    houses.append([address, hometype, price, sold_date, status, area, beds, baths, assessment, zest, link_to_buy])

if 1==1 :
    waits = [1,2,3]
    while (page_number<20):
        page_number+=1
        soup = BeautifulSoup(requests.get(url+str(page_number)+footer, headers=headers).content, "html.parser")
        data = json.loads(
            soup.select_one("script[data-zrr-shared-data-key]")
            .contents[0]
            .strip("!<>-")
        )
        page_data = data['cat1']['searchResults']['listResults']
        time.sleep(random.choice(waits)) #How much to sleep
        #combine page_data to all_data here? Before extracting results
        print(page_number)
        for i in range(len(page_data)):
            count+=1
            try:
                price = page_data[i]['units'][0]['price']
            except KeyError:
                price = page_data[i]['unformattedPrice']
            try:
                assessment = page_data[i]['hdpData']['homeInfo']['taxAssessedValue']
            except KeyError:
                assessment = "Missing"
            try:
                zest = page_data[i]['hdpData']['homeInfo']['zestimate']
            except KeyError:
                zest = "Missing"
            try:
                sold_date = page_data[i]['hdpData']['homeInfo']['dateSold']
            except KeyError:
                sold_date = "Missing"
            try:
                status = all_data[i]['hdpData']['homeInfo']['homeStatus']
            except KeyError:
                status = "Missing"
            hometype = page_data[i]['hdpData']['homeInfo']['homeType']
            address = page_data[i]['address']
            area = page_data[i]['area']
            beds = page_data[i]['beds']
            baths = page_data[i]['baths']

            link = page_data[i]['detailUrl']
            # sometimes the link does not contain the starting website url, thats why we are inserting "https://www.zillow.com{link}" at the starting of link
            if 'http' not in link:
                link_to_buy = "https://www.zillow.com" + link
            else:
                link_to_buy = link
            houses.append([address, hometype, price, sold_date, status, area, beds, baths, assessment, zest, link_to_buy])
            """ print(price)
            print(address)
            print(link_to_buy)
            print(str(beds) + " beds")
            print(str(baths) + " baths")
            print(str(area)+" sqft")
            print(count)
            print("\n") """
    with open('housing_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(houses)
print(len(houses))
