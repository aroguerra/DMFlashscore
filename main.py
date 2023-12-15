import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import re
import scraping_matches

PLAYER_POSITION = DMconf['PLAYER_POSITION']
RESPONSE_STATUS_200 = DMconf['RESPONSE_STATUS_200']
URL = DMconf['URL']

HEADERS = DMcont['HEADERS']
season_urls = [DMconf['season_1'],
               DMconf['season_2'],
               DMconf['season_3'],
               DMconf['season_4'],
               DMconf['season_5']
               ]


def get_season_info(season_url):
    driver = webdriver.Chrome()  # Create a new WebDriver instance for each task
    try:
        driver.get(season_url)  # Perform Selenium interactions
        time.sleep(10)
        season = driver.find_element(By.CLASS_NAME, 'dropdown__selectedValue')
        print(f'SEASON: {season.text}')
        standings_table = driver.find_elements(By.CLASS_NAME, 'ui-table__row')
        if '2024' in season.text:
            anchor = driver.find_element(By.XPATH, '//a[contains(@href, "/form")]')  # button form
            get_team_form_5matches(anchor)
            anchor_squads = driver.find_elements(By.XPATH, '//a[@class="tableCellParticipant__name"]')
            get_team_page(anchor_squads)

        for team_elements in standings_table:
            team_stats = team_elements.text.split('\n')
            print(f"Position:{team_stats[0]}")
            print(
                f"Team Name:{team_stats[1]} matches:{team_stats[2]} W:{team_stats[3]} D:{team_stats[4]} L:{team_stats[5]} GD:{team_stats[6]}")
    except Exception as er:
        print(f'something went wrong {er}')
    finally:
        driver.quit()  # Close the WebDriver instance


def get_team_page(anchor):
    for team in anchor:
        href_value = team.get_attribute('href')
        driver = webdriver.Chrome()
        driver.get(href_value)
        time.sleep(2)
        anchor_squad = driver.find_element(By.XPATH, '//a[contains(@href, "/squad")]')  # button form
        get_players(anchor_squad)


def get_players(anchor):
    href_value = anchor.get_attribute('href')
    driver = webdriver.Chrome()
    driver.get(href_value)
    time.sleep(2)
    players_table = driver.find_elements(By.CLASS_NAME, 'lineup--soccer')
    players_each_pos = players_table[PLAYER_POSITION].find_elements(By.CLASS_NAME, 'lineup__rows')
    for players in players_each_pos:
        players_position = players.find_elements(By.CLASS_NAME, 'lineup__title')
        players_each_position = players.find_elements(By.CLASS_NAME, 'lineup__row')
        for player in players_each_position:
            if players_position[
                PLAYER_POSITION].text != 'Coach':  # change coach logic add get coach (quick fix) add def get_coach
                print(players_position[PLAYER_POSITION].text)
                player_stats = player.text.split('\n')
                print(f"number:{player_stats[0]}")
                print(
                    f"Name:{player_stats[1]} matches:{player_stats[2]} APP:{player_stats[3]} goals:{player_stats[4]} Yc:{player_stats[5]} Rc:{player_stats[6]}")

                # Find the matching SVG elements find_elements(By.XPATH, '//svg[@class="lineup__cell lineup__cell--absence injury"]')


def get_team_form_5matches(anchor):
    href_value = anchor.get_attribute('href')
    driver2 = webdriver.Chrome()
    driver2.get(href_value)
    time.sleep(10)
    print('LAST 5 MATCHES')
    standings_table = driver2.find_elements(By.CLASS_NAME, 'ui-table__row')
    for team_elements in standings_table:
        team_stats = team_elements.text.split('\n')

        print(f"Position:{team_stats[0]}")
        print(
            f"Team Name:{team_stats[1]} matches:{team_stats[2]} W:{team_stats[3]} D:{team_stats[4]} L:{team_stats[5]} GD:{team_stats[6]}")


def main():
    seasons_url_list = scraping_matches.get_list_of_seasons_url(URL, HEADERS)
    for url in season_urls:
        get_season_info(url)
    matches_data_list = scraping_matches.scraping_matches_results(seasons_url_list)


if __name__ == "__main__":
    main()
