import grequests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
import re


RESPONSE_STATUS_200 = 200
URL = 'https://www.flashscore.com/football/england/premier-league/archive/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
                  '/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


def get_list_of_seasons_url(url, headers_a):
    flashscore_archive_response = requests.get(url, headers=headers_a)
    if flashscore_archive_response.status_code == RESPONSE_STATUS_200:
        archive_html_tree = BeautifulSoup(flashscore_archive_response.content, 'html5lib')
        seasons_tag_list = archive_html_tree.find_all('a', attrs={"class": "archive__text archive__text--clickable"},
                                                     href=re.compile(r'/football/england/premier-league*'))
        seasons_url_list = ["https://www.flashscore.com" + line.get("href") for line in seasons_tag_list]
        return seasons_url_list
    else:
        print(f'CRITICAL: Access to webpage denied! No response from webpage.\nStatus code: {imdb_response.status_code}')


def get_matches_url_list(url_list, headers_a):
    match_url_list = []
    for link in url_list:
        indicator = 1
        driver = webdriver.Chrome()
        driver.get(link + 'results/')
        driver.implicitly_wait(5)
        driver.maximize_window()
        button = driver.find_element(By.CLASS_NAME, "event__more--static")
        while indicator == 1:
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", button)
            time.sleep(1)
            button.click()
            time.sleep(1)
            season_response = driver.page_source
            season_html_tree = BeautifulSoup(season_response, 'html.parser')
            show_more_tag = season_html_tree.find('a', attrs={"class": "event__more"})
            if show_more_tag is None:
                indicator = 0
        season_response = driver.page_source
        driver.quit()
        season_html_tree = BeautifulSoup(season_response, 'html.parser')
        match_tag_list = season_html_tree.find_all('div', id=re.compile(r'g_1_*'))
        match_url_new_batch =['https://www.flashscore.com/match/' + match_tag.get("id").lstrip('g_1_') + '/#/match-summary/match-summary' for match_tag in match_tag_list]
        match_url_list += match_url_new_batch
    return match_url_list


def get_match_data(url_list, headers_a):
    matches_data_list = []
    for link_url in url_list:
        driver = webdriver.Chrome()
        driver.get(link_url)
        driver.implicitly_wait(5)
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
    return matches_data_list


def main():
    seasons_url_list = get_list_of_seasons_url(URL, headers)
    short_season_url_list = [seasons_url_list[1]]
    match_url_list = get_matches_url_list(short_season_url_list, headers)
    match_data_list = get_match_data(match_url_list, headers)
    for match in match_data_list:
        print(f'Match date: {match[0]}   Home team: {match[1]}   Home team score: {match[2]}   Away team: {match[3]}   Away team score:{match[4]}')


if __name__ == '__main__':
    main()