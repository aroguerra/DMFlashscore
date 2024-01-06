from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import json
import logging
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

with open('DMconf.json', 'r') as config_file:
    config = json.load(config_file)

RESPONSE_STATUS_200 = config['RESPONSE_STATUS_200']
URL = config['URL']
HEADERS = config['HEADERS']
INDICATOR = config['INDICATOR']
WAIT5 = config['WAIT5']
SLEEP1 = config['SLEEP1']
DATE_FORMAT = config['DATE_FORMAT']

logger = logging.getLogger('flashscore')

# service = Service('./chromedriver')
service = ChromeService(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED on Linux
chrome_options.add_argument('--headless')
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems


def get_list_of_seasons_url(url, headers_a):
    """
    retrieves a list of urls including the urls for all the seasons web pages.
    :param url: the url address for the Flashscore archive web page.
    :type url: str
    :param headers_a: a header for requests module to work around webpage scraping limitations
    :type headers_a: str
    :return: list of urls for each each season web page
    """
    flashscore_archive_response = requests.get(url, headers=headers_a)
    if flashscore_archive_response.status_code == RESPONSE_STATUS_200:
        archive_html_tree = BeautifulSoup(flashscore_archive_response.content, 'html5lib')
        seasons_tag_list = archive_html_tree.find_all('a', attrs={"class": "archive__text archive__text--clickable"},
                                                      href=re.compile(r'/football/england/premier-league*'))
        seasons_url_list = ["https://www.flashscore.com" + line.get("href") for line in seasons_tag_list]
        logger.debug("Scrapped seasons urls pages of matches successfully")
        return seasons_url_list
    else:
        logger.error(
            f'CRITICAL: Access to webpage denied! No response from webpage.\nStatus code: {flashscore_archive_response.status_code}')


def get_matches_url_list(url_list):
    """
    retrives a list of urls for all the season's matches web pages.
    :param url_list: list of season's urls
    :type url_list: list
    :return: list of urls for each season's match webpage.
    """
    match_url_list = []
    for link in url_list:
        indicator = INDICATOR
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver.get(link + 'results/')
        driver.implicitly_wait(WAIT5)
        driver.maximize_window()
        button = driver.find_element(By.CLASS_NAME, "event__more--static")
        while indicator == INDICATOR:
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", button)
            time.sleep(SLEEP1)
            button.click()
            time.sleep(SLEEP1)
            season_response = driver.page_source
            season_html_tree = BeautifulSoup(season_response, 'html.parser')
            show_more_tag = season_html_tree.find('a', attrs={"class": "event__more"})
            if show_more_tag is None:
                indicator = 0
        season_response = driver.page_source
        driver.quit()
        season_html_tree = BeautifulSoup(season_response, 'html.parser')
        match_tag_list = season_html_tree.find_all('div', id=re.compile(r'g_1_*'))
        match_url_new_batch = [
            'https://www.flashscore.com/match/' + match_tag.get("id").lstrip('g_1_') + '/#/match-summary/match-summary'
            for match_tag in match_tag_list]
        match_url_list += match_url_new_batch
    logger.debug("Scrapped urls pages of matches successfully")
    return match_url_list


def get_match_data(url_list):
    """
    retrieves match date, participanting teams and match scores for each match
    :param url_list: list of matches web pages urls
    :type url_list: list
    :return: a list of lists, where each list represents a match with the match date, participating teams and scores.
    """
    matches_data_list = []
    for link_url in url_list:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        driver.get(link_url)
        driver.implicitly_wait(WAIT5)
        match_summary_response = driver.page_source
        driver.quit()
        match_html_tree = BeautifulSoup(match_summary_response, 'html5lib')
        match_date_tag = match_html_tree.find_all('div', attrs={"class": "duelParticipant__startTime"})
        match_date = match_date_tag[0].get_text(strip=True)
        teams_tag_list = match_html_tree.find_all('a', attrs={"class": "participant__participantName"})
        teams_list = [tag.get_text(strip=True) for tag in teams_tag_list]
        score_tag = match_html_tree.find_all('div', attrs={"class": "detailScore__wrapper"})
        score = score_tag[0].get_text(strip=True)
        match_detail_list = [match_date[0:10], teams_list[0], score[0], teams_list[1], score[2]]
        matches_data_list.append(match_detail_list)
    logger.debug("Scrapped matches data and information successfully")
    return matches_data_list


def scraping_matches_results():
    """
    Retrieves a list of all the matches and their final scores.
    :return: a list of lists, where each list represents a single match withe the event date, the participaiting
    teams and the scores
    """
    matches = []
    seasons_url_list = get_list_of_seasons_url(URL, HEADERS)
    short_season_url_list = seasons_url_list[0:1]
    match_url_list = get_matches_url_list(short_season_url_list)
    match_data_list = get_match_data(match_url_list)
    for match in match_data_list:
        matches.append([
            datetime.strptime(match[0], DATE_FORMAT),
            match[1],
            match[2],
            match[3],
            match[4]
        ])
    logger.info("Scrapped all matches successfully")
    return matches
