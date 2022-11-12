"""
Dependencies listed below
------------------------------------------
async-generator==1.10
attrs==21.4.0
beautifulsoup4==4.11.1
certifi==2022.6.15
cffi==1.15.1
charset-normalizer==2.1.0
comtypes==1.1.11
cryptography==37.0.4
h11==0.13.0
idm==0.39
idna==3.3
outcome==1.2.0
pycparser==2.21
pyOpenSSL==22.0.0
pypiwin32==223
PySocks==1.7.1
pywin32==304
requests==2.28.1
selenium==4.3.0
sniffio==1.2.0
sortedcontainers==2.4.0
soupsieve==2.3.2.post1
trio==0.21.0
trio-websocket==0.9.2
urllib3==1.26.10
wsproto==1.1.0
------------------------------------------
NOTE: You will need to install Firefox and geckodriver for this script to work as it uses Selenium based on FireFox bypass the captcha.
NOTE: Downloading more than two episodes at a time will prompt captcha, and it will have to be autocompleted.
NOTE: You MUST have Internet Download Manager installed for this script to work.

To download all episodes of a show, run.
python3 www1.myasiantv.py <show_id>

To download a specific episode of a show, run.
python3 www1.myasiantv.py <show_id> <episode_number>

To get the show_id, go on www1.myasiantv.cc, search for your TV show and then copy the id as displayed in the URL.
For example, if the URL is www1.myasiantv.cc/show/flower-of-evil, then the show_id is flower-of-evil.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from idm import IDMan
from time import sleep
from bs4 import BeautifulSoup
import requests, os, sys

BASE_URL = "https://www1.myasiantv.cc/show/"
downloader = IDMan()
DOWNLOAD_DIRECTORY = "C:\\Users\\Ashwi\\Downloads\\KDrama"
SAVE_DIRECTORY = "E:\\Media\\DocsTransfer\\TV Shows\\K Drama"

def has_episode_been_downloaded(show, name):
    if os.path.exists(DOWNLOAD_DIRECTORY + "\\" + name):
        return True
    elif os.path.exists(SAVE_DIRECTORY + "\\" + show + "\\" + name):
        return True
    else:
        return False

def get_episodes(show):
    url = BASE_URL + show
    r = requests.get(url)
    episode_urls = []
    soup = BeautifulSoup(r.text, 'html.parser')
    max_episodes = int(soup.select('ul.list-episode')[0].find_all('li')[0].find('a').text[-2:]) # Get's the episode number of the latest episode
    
    # Some shows have Episode 0, but they're usually RAW, and have no subtitles
    for n in range(1, max_episodes+1):
        episode_urls.append(f"{url}/episode-{n}")
    return episode_urls

def get_cdn_link(episode_url):
    browser = webdriver.Firefox()
    browser.get(episode_url)
    try:
        try:
            print("Checking captcha presence...")
            while WebDriverWait(browser, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="captcha-v2"]'))):
                print("Captcha detected. Checking again 5 seconds...")
                sleep(5)
        except:
            print("Waiting for download links to load...")
            WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/section/div/div[2]/div/div[4]/div[1]")))     
    finally:
        pass

    r = browser.page_source
    browser.close()
    soup = BeautifulSoup(r, 'html.parser')
    download_link = soup.select('div.mirror_link')[0]
    a_tags = download_link.find_all('a')
    cdn_highest_quality = a_tags[-1]['href']
    quality = a_tags[-1].text.replace('Download (', '').replace(' - mp4)', '')
    print("Found highest quality: " + quality.replace('Download (', '').replace(' - mp4)', ''))
    return cdn_highest_quality, episode_url

def get_ep_download_link(download_link):
    r = requests.get(download_link)
    soup = BeautifulSoup(r.text, 'html.parser')
    cdn_link = soup.select('a.download')[0]['href']
    return cdn_link

if __name__ == "__main__":

    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python3 www1.myasiantv.cc.py <show id> <download_method> <episode>\nDownload methods: aria2c, idm")
        sys.exit(1)
    show = sys.argv[1]
    
    if sys.argv[2].lower() != "idm" and sys.argv[2].lower() != "aria2c":
        print("Invalid download method, available methods are: aria2c, idm")
        sys.exit(1)
    
    episode_urls = get_episodes(show)
    print(str(len(episode_urls)) + " episodes found for " + show)
    i = 0

    try:
        if sys.argv[3] != "":
            episode = int(sys.argv[3])
            print("-"*50)
            episode_url = episode_urls[episode-1]
            if has_episode_been_downloaded(show, f"{show}-{episode}.mp4"):
                print(f"{show}-{episode}.mp4 already downloaded, skipping...")
                sys.exit(0)
            print("Starting episode " + str(episode))
            download = get_ep_download_link(episode_url)
            cdn_link = get_cdn_link("http:" + download)
            print(f"Downloading: {show}-{episode}.mp4")
            
            if sys.argv[2].lower() == "idm":
                downloader.download(cdn_link[0], DOWNLOAD_DIRECTORY ,output=f"{show}-{episode}.mp4", referrer=cdn_link[1], cookie=None, postData=None, user=None, password=None, confirm=False, lflag=None, clip=False)
                sys.exit(1)
            
            elif sys.argv[2].lower() == "aria2c":
                os.system(f"aria2c --max-tries=10 --max-connection-per-server=10 --retry-wait=10 --referer={cdn_link[1]} --continue --split=10 --dir={DOWNLOAD_DIRECTORY} --out={show}-{episode}.mp4 {cdn_link[0]}")
                sys.exit(1)
            print("-"*50)
            
    except:
        print("No episode number provided, downloading all episodes")
    
    if not os.path.exists(DOWNLOAD_DIRECTORY):
        os.mkdir(DOWNLOAD_DIRECTORY)

    for episode_url in episode_urls:
        print("-"*50)
        i += 1
        if has_episode_been_downloaded(show, f"{show}-{i}.mp4"):
            print(f"{show}-{i}.mp4 already downloaded, skipping...")
            continue
        print("Starting episode " + str(i) + " of " + str(len(episode_urls)))
        download = get_ep_download_link(episode_url)
        cdn_link = get_cdn_link("http:" + download)
        print(f"Downloading: {show}-{i}.mp4 / ({str(i)}/{str(len(episode_urls))})")
        
        if sys.argv[2].lower() == "idm":
            downloader.download(cdn_link[0], DOWNLOAD_DIRECTORY ,output=f"{show}-{i}.mp4", referrer=cdn_link[1], cookie=None, postData=None, user=None, password=None, confirm=False, lflag=None, clip=False)
        
        elif sys.argv[2].lower() == "aria2c":
            os.system(f"aria2c --max-tries=10 --max-connection-per-server=10 --retry-wait=10 --referer={cdn_link[1]} --continue --split=10 --dir={DOWNLOAD_DIRECTORY} --out={show}-{i}.mp4 {cdn_link[0]}")
        
        sleep(5)
