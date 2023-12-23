import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import logging

with open('DMconf.json', 'r') as config_file:
    config = json.load(config_file)

PLAYER_POSITION = config['PLAYER_POSITION']
SLEEP10 = config['SLEEP10']
SLEEP2 = config['SLEEP2']
SEASON_YEAR = config['SEASON_YEAR']
COACH_LIST = config['COACH_LIST']

logger = logging.getLogger('flashscore')


def get_team_page(season_url):
    """
    Retrieves a list of all players from each team's page for the current season.
    :param season_url: The URL of the season's main page
    :type season_url: str
    :return: all players list of the season
    """
    players_list = []
    driver = webdriver.Chrome()
    driver.get(season_url)
    time.sleep(SLEEP2)
    season = driver.find_element(By.CLASS_NAME, 'dropdown__selectedValue')
    if SEASON_YEAR in season.text:
        anchor_squads = driver.find_elements(By.XPATH, '//a[@class="tableCellParticipant__name"]')
        for team in anchor_squads:
            href_value = team.get_attribute('href')
            driver = webdriver.Chrome()
            driver.get(href_value)
            time.sleep(SLEEP2)
            anchor_squad = driver.find_element(By.XPATH, '//a[contains(@href, "/squad")]')  # button form
            logger.debug('Scrapped teams page successfully')
            players_list.append(get_players(anchor_squad, team.text))
    logger.info('Scrapped team players successfully')
    return players_list


def get_players(anchor, team):
    """
    Retrieves the list of players from a given team and his stats
    :param anchor: html anchor
    :type anchor: str
    :param team: team name
    :type team: str
    :return: players list of a single team
    """
    team_players = []
    href_value = anchor.get_attribute('href')
    driver = webdriver.Chrome()
    driver.get(href_value)
    time.sleep(SLEEP2)
    players_table = driver.find_elements(By.CLASS_NAME, 'lineup--soccer')
    players_each_pos = players_table[PLAYER_POSITION].find_elements(By.CLASS_NAME, 'lineup__rows')
    for players in players_each_pos:
        players_position = players.find_elements(By.CLASS_NAME, 'lineup__title')
        players_each_position = players.find_elements(By.CLASS_NAME, 'lineup__row')
        for player in players_each_position:
            if players_position[PLAYER_POSITION].text != COACH_LIST:
                # player.find_elements(By.XPATH, '//svg[@class="lineup__cell lineup__cell--absence injury"]')
                player_stats = player.text.split('\n')
                team_players.append([
                    team,
                    player_stats[1],
                    0,
                    player_stats[2],
                    players_position[PLAYER_POSITION].text,
                    player_stats[4],
                    player_stats[5],
                    player_stats[6]
                ])

    return team_players
