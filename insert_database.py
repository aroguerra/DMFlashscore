import mysql.connector
import json
import logging

with open('DMconf.json', 'r') as config_file:
    config = json.load(config_file)

HOST = config['HOST']
USER = config['USER']
PASSWORD = config['PASSWORD']
DATABASE = config['DATABASE']

connection = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

cursor = connection.cursor()

logger = logging.getLogger('flashscore')

def use_db():
    """
    SQL query to use the flashscore Database
    """
    with connection.cursor() as cursor:
        teams_insert_query = "USE flashscore;"
        cursor.execute(teams_insert_query)
        connection.commit()
        logger.debug("SQL query executed successfully")


def get_team(teams_list):
    """
    Gets a list that has the teams names and retrieves the same list after changing the teams names by their ID's
    :param teams_list: list of teams or players
    :type teams_list: list
    :return: same list but with teams ID's instead of names
    """
    use_db()
    for team in teams_list:
        teams_insert_query = """
            SELECT id
            FROM teams
            WHERE team_name = %s"""
        try:
            cursor.execute(teams_insert_query, (team[0],))
            result = cursor.fetchone()
            if result:
                team[0] = result[0]
        except Exception as e:
            print(f"Error: {e}")
    logger.debug("Teams ID's changed successfully")
    return teams_list


# Establish a connection to MySQL

def insert_teams(teams_list):
    """
    SQL query to insert teams on database
    :param teams_list: list of teams names
    :type teams_list: list
    """
    use_db()
    with connection.cursor() as cursor:
        teams_insert_query = "INSERT INTO `teams` (`team_name`) VALUES (%s)"
        cursor.executemany(teams_insert_query, teams_list)
        connection.commit()
        logger.debug("SQL query executed successfully")


def insert_standings(standings_list):
    """
    SQL query to insert standings on database
    :param standings_list: list of teams standings seasons
    :type standings_list: list
    """
    use_db()
    result = get_team(standings_list)
    with connection.cursor() as cursor:
        teams_insert_query = """INSERT INTO `standings_five_seasons` 
        (`team_id`, `table_position`, `matches_played`, `wins`, `draws`, `losses`, `goals_scored`, `goals_suffered`, `year`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(teams_insert_query, result)
        connection.commit()
        logger.debug("SQL query executed successfully")


def insert_form_5matches(form_list):
    """
    SQL query to insert form of last 5 matches on database
    :param form_list: list of teams last 5 matches form
    :type form_list: list
    """
    use_db()
    result = get_team(form_list)
    with connection.cursor() as cursor:
        teams_insert_query = """INSERT INTO `form_last_five_matches` 
        (`team_id`, `matches_played`, `wins`, `draws`, `losses`, `goals_scored`, `goals_suffered`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(teams_insert_query, result)
        connection.commit()
        logger.debug("SQL query executed successfully")


def insert_players(players_list):
    """
    SQL query to insert players from teams on database
    :param players_list: list with the players of scrapped teams
    :type players_list: list
    """
    use_db()
    result = get_team(players_list)
    with connection.cursor() as cursor:
        teams_insert_query = """INSERT INTO `players` 
        (`team_id`, `player_name`, `injury`, `age`, `field_position`, `goals_scored`, `yellow_cards`, `red_cards`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(teams_insert_query, result)
        connection.commit()
        logger.debug("SQL query executed successfully")


def get_team_matches(matches_list):
    """
    Gets a list that has matches and retrieves the same list after changing the teams names by their ID's
    :param matches_list: list of matches
    :type matches_list: list
    :return: same list but with teams ID's instead of names
    """
    use_db()
    for match in matches_list:
        teams_insert_query = """
            SELECT id
            FROM teams
            WHERE team_name = %s"""
        try:
            cursor.execute(teams_insert_query, (match[1],))
            result1 = cursor.fetchone()
            cursor.execute(teams_insert_query, (match[3],))
            result2 = cursor.fetchone()
            if result1 and result2:
                match[1] = result1[0]
                match[3] = result2[0]
        except Exception as e:
            print(f"Error: {e}")
    logger.debug("Teams ID's changed successfully")
    return matches_list


def insert_matches(matches_list):
    """
    SQL query to insert matches on database
    :param matches_list: list of matches between the teams with results
    :type matches_list: list
    """
    use_db()
    result = get_team_matches(matches_list)
    with connection.cursor() as cursor:
        teams_insert_query = """INSERT INTO `matches` 
        (`match_date`, `team1_id`, `goals_scored_team1`, `team2_id`, `goals_scored_team2`) 
        VALUES (%s, %s, %s, %s, %s)"""
        cursor.executemany(teams_insert_query, result)
        connection.commit()
        logger.debug("SQL query executed successfully")


def insert_future_fixtures_predictions(predictions_list):
    use_db()
    for ind, prediction in enumerate(predictions_list):
        teams_id_query = """SELECT id
                            FROM teams
                            WHERE teams_name 
                            LIKE CONCAT(%, %s, %)"""
        cursor.execute(teams_id_query, (predictions_list[0],))
        result1 = cursor.fetchone()
        cursor.execute(teams_id_query, (predictions_list[1],))
        result2 = cursor.fetchone()
        if result1 and result2:
            prediction[0] = result1[0]
            prediction[1] = result2[0]
            predictions_list[ind] = prediction
    predictions_insert_query = """INSERT INTO `future_fixtures_predictions_data`
    (`home_team_id`, `away_team_id`, `prediction_home_team_wins`, `prediction_draw`, `prediction_away_team_wind`)
    VALUES (%s, %s, %s, %s, %s)"""
    cursor.executemany(predictions_insert_query, predictions_list)
    connection.commit()
    logger.debug("SQL query executed successfully")
