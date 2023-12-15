import mysql.connector
import json

with open('DMconf.json', 'r') as config_file:
    config = json.load(config_file)

HOST = config['HOST']
USER = config['USER']
PASSWORD = config['PASSWORD']
DATABASE = config['DATABASE']
sql_file_path = 'flash.sql'

connection = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

cursor = connection.cursor()


def use_db():
    with connection.cursor() as cursor:
        teams_insert_query = "USE flashscore;"
        cursor.execute(teams_insert_query)
        connection.commit()


def get_team(teams_list):
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
    return teams_list


# Establish a connection to MySQL

def insert_teams(teams_list):
    use_db()
    with connection.cursor() as cursor:
        teams_insert_query = "INSERT INTO `teams` (`team_name`) VALUES (%s)"
        cursor.executemany(teams_insert_query, teams_list)
        connection.commit()


def insert_standings(teams_list):
    use_db()
    result = get_team(teams_list)
    with connection.cursor() as cursor:
        teams_insert_query = """INSERT INTO `standings_five_seasons` 
        (`team_id`, `table_position`, `matches_played`, `wins`, `draws`, `losses`, `goals_scored`, `goals_suffered`, `year`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(teams_insert_query, result)
        connection.commit()


def insert_form_5matches(teams_list):
    use_db()
    result = get_team(teams_list)
    with connection.cursor() as cursor:
        teams_insert_query = """INSERT INTO `form_last_five_matches` 
        (`team_id`, `matches_played`, `wins`, `draws`, `losses`, `goals_scored`, `goals_suffered`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(teams_insert_query, result)
        connection.commit()


def insert_players(players):
    use_db()
    result = get_team(players)
    with connection.cursor() as cursor:
        teams_insert_query = """INSERT INTO `players` 
        (`team_id`, `player_name`, `injury`, `age`, `field_position`, `goals_scored`, `yellow_cards`, `red_cards`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.executemany(teams_insert_query, result)
        connection.commit()


def get_team_matches(matches):
    use_db()
    for match in matches:
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
    return matches


def insert_matches(matches):
    use_db()
    result = get_team_matches(matches)
    with connection.cursor() as cursor:
        teams_insert_query = """INSERT INTO `matches` 
        (`match_date`, `team1_id`, `goals_scored_team1`, `team2_id`, `goals_scored_team2`) 
        VALUES (%s, %s, %s, %s, %s)"""
        cursor.executemany(teams_insert_query, result)
        connection.commit()
