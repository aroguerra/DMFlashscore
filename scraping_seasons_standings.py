import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import logging
from selenium.webdriver.chrome.service import Service

with open('DMconf.json', 'r') as config_file:
    config = json.load(config_file)

SLEEP10 = config['SLEEP10']
SEASON_YEAR = config['SEASON_YEAR']
COACH_LIST = config['COACH_LIST']

logger = logging.getLogger('flashscore')

service = Service('./chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("--headless")


def get_season_info(season_url):
    """
    Retrieves the list with all teams season's information and a list with all the teams of the season
    :param season_url: The URL of the season's main page
    :type season_url: str
    :return: a list of the season's information and the teams of the season
    """
    teams = []
    standings = []
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(season_url)
        time.sleep(SLEEP10)
        season = driver.find_element(By.CLASS_NAME, 'dropdown__selectedValue')
        standings_table = driver.find_elements(By.CLASS_NAME, 'ui-table__row')
        for team_elements in standings_table:
            team_stats = team_elements.text.split('\n')
            teams.append((team_stats[1],))
            standings.append([
                team_stats[1],
                team_stats[0],
                team_stats[2],
                team_stats[3],
                team_stats[4],
                team_stats[5],
                team_stats[6].split(':')[0],
                team_stats[6].split(':')[1],
                season.text
            ])
        logger.info('Scrapped teams and standings successfully')
        return teams, standings

    except Exception as er:
        print(f'something went wrong {er}')
    finally:
        driver.quit()
