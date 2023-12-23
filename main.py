import argparse
import db_connect
import insert_database
import scraping_matches
import scraping_seasons_standings
import scraping_form_5matches
import scraping_players
import json
import logging


logger = logging.getLogger('flashscore')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')
file_handler = logging.FileHandler('flashscore.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

with open('DMconf.json', 'r') as config_file:
    config = json.load(config_file)

PLAYER_POSITION = config['PLAYER_POSITION']
RESPONSE_STATUS_200 = config['RESPONSE_STATUS_200']
URL = config['URL']
SEASON_URLS = config['SEASON_URLS']
HEADERS = config['HEADERS']
SLEEP10 = config['SLEEP10']
SLEEP2 = config['SLEEP2']
SEASON_YEAR = config['SEASON_YEAR']
COACH_LIST = config['COACH_LIST']


def main():
    teams = []
    standings = []
    form_5matches = []
    players_list = []
    matches = []
    parser = argparse.ArgumentParser()
    parser.add_argument("-all", "-a", help="fetch all scrapped data", action="store_true")
    parser.add_argument("-seasons", "-s", help="fetch last 5 seasons data", action="store_true")
    parser.add_argument("-matches", "-m", help="fetch all scrapped data", action="store_true")
    parser.add_argument("-players", "-p", help="fetch players data", action="store_true")
    parser.add_argument("-form", "-f", help="fetch form last 5 matches data", action="store_true")
    parser.add_argument("-teams", "-t", help="fetch teams data", action="store_true")

    #### WITH ARGPARSE ############
    args = parser.parse_args()
    db_connect.create_db()
    if args.all:
        print('fetch all')
        for url in SEASON_URLS:
            result = scraping_seasons_standings.get_season_info(url)
            teams.append(result[0])
            standings.append(result[1])
            form_5matches.append(scraping_form_5matches.get_team_form_5matches(url))
            players_list.append(scraping_players.get_team_page(url))
        matches.append(scraping_matches.scraping_matches_results())
        logger.info("Fetched all data successfully")
        insert_database.insert_teams(list(set(sum(teams, []))))
        insert_database.insert_standings(sum(standings, []))
        insert_database.insert_matches(matches[0])  # check for more than season!!!!!!!!!!!
        insert_database.insert_form_5matches(form_5matches[0])
        insert_database.insert_players(sum(players_list[0], []))
        logger.info("Inserted all in the database")
    elif args.seasons:
        print('fetch standings')
        for url in SEASON_URLS:
            result = scraping_seasons_standings.get_season_info(url)
            teams.append(result[0])
            standings.append(result[1])
        logger.info("Fetched teams and seasons successfully")
        insert_database.insert_teams(list(set(sum(teams, []))))
        insert_database.insert_standings(sum(standings, []))
        print('fetched standings')
        logger.info("Inserted teams and seasons in the database")
    elif args.matches:
        print('fetch matches')
        for url in SEASON_URLS:
            result = scraping_seasons_standings.get_season_info(url)
            teams.append(result[0])
        matches.append(scraping_matches.scraping_matches_results())
        logger.info("Fetched matches successfully")
        insert_database.insert_teams(list(set(sum(teams, []))))
        insert_database.insert_matches(matches[0])  # check for more than season!!!!!!!!!!!!!!!
        logger.info("Inserted teams and matches in the database")
    elif args.players:
        print('fetch players')
        for url in SEASON_URLS:
            result = scraping_seasons_standings.get_season_info(url)
            teams.append(result[0])
            players_list.append(scraping_players.get_team_page(url))
        logger.info("Fetched players successfully")
        insert_database.insert_teams(list(set(sum(teams, []))))
        insert_database.insert_players(sum(players_list[0], []))
        logger.info("Inserted teams and players in the database")
    elif args.form:
        print('fetch form last 5 matches')
        for url in SEASON_URLS:
            result = scraping_seasons_standings.get_season_info(url)
            teams.append(result[0])
            form_5matches.append(scraping_form_5matches.get_team_form_5matches(url))
        logger.info("Fetched form of last 5 matches successfully")
        insert_database.insert_teams(list(set(sum(teams, []))))
        insert_database.insert_form_5matches(form_5matches[0])
        logger.info("Inserted teams and form of last 5 matches in the database")
    elif args.teams:
        print('fetch teams')
        for url in SEASON_URLS:
            result = scraping_seasons_standings.get_season_info(url)
            teams.append(result[0])
        logger.info("Fetched teams successfully")
        insert_database.insert_teams(list(set(sum(teams, []))))
        logger.info("Inserted teams in the database")

    else:
        logger.error("Requires an argument to perform an action")
        print("Error:Requires an argument to perform an action")

    #### WITHOUT ARGPARSE ############
    # db_connect.create_db()
    # for url in SEASON_URLS:
    #     result = scraping_seasons_standings.get_season_info(url)
    #     teams.append(result[0])
    #     # standings.append(result[1])
    #     # form_5matches.append(scraping_form_5matches.get_team_form_5matches(url))
    #     # players_list.append(scraping_players.get_team_page(url))
    # matches.append(scraping_matches.scraping_matches_results())

    # print(teams)
    # print(standings)
    # print(form_5matches)
    # print(players_list)
    # print('here')
    # insert_database.insert_teams(list(set(sum(teams, []))))
    # insert_database.insert_standings(sum(standings, []))
    # insert_database.insert_form_5matches(form_5matches[0])
    # insert_database.insert_players(sum(players_list[0], []))
    # insert_database.insert_matches(matches[0]) # check for more than season


