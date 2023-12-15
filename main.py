import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
import db_connect
import insert_database
import scraping_matches
import json


with open('DMconf.json', 'r') as config_file:
    config = json.load(config_file)


PLAYER_POSITION = config['PLAYER_POSITION']
RESPONSE_STATUS_200 = config['RESPONSE_STATUS_200']
URL = config['URL']

HEADERS = config['HEADERS']
season_urls = [config['season_1'],
               config['season_2'],
               config['season_3'],
               config['season_4'],
               config['season_5']
               ]
SLEEP10 = config['SLEEP10']
SLEEP2 = config['SLEEP2']

TEAMS = []
STANDINGS = []
FORM_5MATCHES = []
PLAYERS_LIST = []



def get_season_info(season_url):
    driver = webdriver.Chrome()  # Create a new WebDriver instance for each task
    try:
        driver.get(season_url)  # Perform Selenium interactions
        time.sleep(SLEEP10)
        season = driver.find_element(By.CLASS_NAME, 'dropdown__selectedValue')
        print(f'SEASON: {season.text}')
        standings_table = driver.find_elements(By.CLASS_NAME, 'ui-table__row')
        for team_elements in standings_table:
            team_stats = team_elements.text.split('\n')
            TEAMS.append((team_stats[1],))
            STANDINGS.append([
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
            # print(f"Position:{team_stats[0]}")
            # print(
            #     f"Team Name:{team_stats[1]} matches:{team_stats[2]} W:{team_stats[3]} D:{team_stats[4]} L:{team_stats[5]} GD:{team_stats[6]}")

        if '2024' in season.text:
            anchor = driver.find_element(By.XPATH, '//a[contains(@href, "/form")]')  # button form
            get_team_form_5matches(anchor)
            anchor_squads = driver.find_elements(By.XPATH, '//a[@class="tableCellParticipant__name"]')
            get_team_page(anchor_squads)

    except Exception as er:
        print(f'something went wrong {er}')
    finally:
        driver.quit()  # Close the WebDriver instance


def get_team_page(anchor):
    for team in anchor:
        href_value = team.get_attribute('href')
        driver = webdriver.Chrome()
        driver.get(href_value)
        time.sleep(SLEEP2)
        anchor_squad = driver.find_element(By.XPATH, '//a[contains(@href, "/squad")]')  # button form
        get_players(anchor_squad, team.text)


def get_players(anchor, team):
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
            if players_position[PLAYER_POSITION].text != 'Coach':  # change coach logic (quick fix)
                player_stats = player.text.split('\n')
                PLAYERS_LIST.append([
                    team,
                    player_stats[1],
                    0,
                    # Find the matching SVG elements find_elements(By.XPATH, '//svg[@class="lineup__cell lineup__cell--absence injury"]')
                    player_stats[2],
                    players_position[PLAYER_POSITION].text,
                    player_stats[4],
                    player_stats[5],
                    player_stats[6]
                ])

                # print(players_position[PLAYER_POSITION].text)
                # player_stats = player.text.split('\n')
                # print(f"number:{player_stats[0]}")
                # print(
                #     f"Name:{player_stats[1]} age:{player_stats[2]} matches:{player_stats[3]} goals:{player_stats[4]} Yc:{player_stats[5]} Rc:{player_stats[6]}")


def get_team_form_5matches(anchor):
    href_value = anchor.get_attribute('href')
    driver2 = webdriver.Chrome()
    driver2.get(href_value)
    time.sleep(SLEEP10)
    print('LAST 5 MATCHES')
    standings_table = driver2.find_elements(By.CLASS_NAME, 'ui-table__row')
    for team_elements in standings_table:
        team_stats = team_elements.text.split('\n')
        FORM_5MATCHES.append([
            team_stats[1],
            team_stats[2],
            team_stats[3],
            team_stats[4],
            team_stats[5],
            team_stats[6].split(':')[0],
            team_stats[6].split(':')[1],
        ])

        # print(f"Position:{team_stats[0]}")
        # print(
        #     f"Team Name:{team_stats[1]} matches:{team_stats[2]} W:{team_stats[3]} D:{team_stats[4]} L:{team_stats[5]} GD:{team_stats[6]}")


def main():
    for url in season_urls:
        get_season_info(url)
    # print(teams)
    # print(standings)
    # print(form_5matches)
    # print(players_list)

    insert_database.insert_teams(list(set(TEAMS)))
    insert_database.insert_standings(STANDINGS)
    insert_database.insert_form_5matches(FORM_5MATCHES)
    insert_database.insert_players(PLAYERS_LIST)
    scraping_matches.scraping_matches_results()


if __name__ == "__main__":
    main()
