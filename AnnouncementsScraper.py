import requests
import time
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import csv
def buildUrl(link):
    #Using the href gathered from the scrapeIndex method to build an accessible url
    baseUrl = "https://www.gov.uk"
    url = baseUrl + link
    return url
    print()

def scrapeIndex():
    links = []
    urls = []
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
    baseUrlToScrape = "https://www.gov.uk/government/announcements?announcement_filter_option=all&departments%5B%5D=all&from_date=&keywords=&page={}&people%5B%5D=all&subtaxons%5B%5D=all&taxons%5B%5D=all&to_date=&world_locations%5B%5D=all"
    for i in range(1,4):
    
        urlToScrape = baseUrlToScrape.format(str(i))
        print(urlToScrape)
        pageResponse = requests.get(urlToScrape, timeout=5, headers=headers)
        soup = BeautifulSoup(pageResponse.content, "html.parser")
        announcements = soup.find_all('a')
        for link in announcements:
    
            if link.get('href')[:16] == '/government/news':
                links.append(link.get('href'))
                print(link.get('href'))
        
    for link in links:
        url = buildUrl(link)
        urls.append(url)
    time.sleep(2)
    return urls

def scrapeArticles(listOfURLS):
    articles = [["TITLE", "PUBLISH_DATE", "IMAGE_URL", "CONTENT"]]
    headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}
    for url in listOfURLS:
        pageResponse = requests.get(url, timeout=5, headers=headers)
        soup = BeautifulSoup(pageResponse.content, "html.parser")
        title = soup.find('h1').text
        publishDate = soup.find('div', attrs={'class':'app-c-published-dates'}).text
        
        image=soup.find('img', attrs={'class':'app-c-figure__image'}).get('src')

        
        content = soup.find('div', attrs={'class':'govspeak'}).text
        
        article = [title, publishDate, image, content]
        articles.append(article)
        #Unnecessary -> just a progress bar
        total, current = len(listOfURLS), listOfURLS.index(url)
        percentComplete = round((current/total)*100)
        print("---------------[Scraping "+str(percentComplete)+"% Complete]---------------")

        time.sleep(2)
    return articles



articleData = scrapeArticles(scrapeIndex())
with open("articles.csv", "a") as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(articleData)