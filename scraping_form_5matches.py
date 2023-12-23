import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import logging

with open('DMconf.json', 'r') as config_file:
    config = json.load(config_file)

SLEEP10 = config['SLEEP10']
SEASON_YEAR = config['SEASON_YEAR']

logger = logging.getLogger('flashscore')


def get_team_form_5matches(season_url):
    """
    Retrieves the list with all teams form for the last 5 matches played on the current season
    :param season_url: The URL of the season's main page
    :type season_url: str
    :return: list with all teams form for the last 5 matches
    """
    form_5matches = []
    driver = webdriver.Chrome()
    driver.get(season_url)
    time.sleep(SLEEP10)
    season = driver.find_element(By.CLASS_NAME, 'dropdown__selectedValue')
    if SEASON_YEAR in season.text:
        anchor_form = driver.find_element(By.XPATH, '//a[contains(@href, "/form")]')  # button form
        href_value = anchor_form.get_attribute('href')
        driver2 = webdriver.Chrome()
        driver2.get(href_value)
        time.sleep(SLEEP10)
        standings_table = driver2.find_elements(By.CLASS_NAME, 'ui-table__row')
        for team_elements in standings_table:
            team_stats = team_elements.text.split('\n')
            form_5matches.append([
                team_stats[1],
                team_stats[2],
                team_stats[3],
                team_stats[4],
                team_stats[5],
                team_stats[6].split(':')[0],
                team_stats[6].split(':')[1],
            ])
        logger.info("Scrapped form of last 5 matches successfully")
        return form_5matches
