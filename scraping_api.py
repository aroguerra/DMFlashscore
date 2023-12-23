from datetime import datetime, timedelta
import json
import requests
import re
import logging

with open('DMconf.json', 'r') as config_file:
    config = json.load(config_file)

DAYS = config['DAYS']
RESPONSE_STATUS_CODE = config['RESPONSE_STATUS_200']
RESPONSE_DATA_LIST = config['RESPONSE_DATA_LIST']
ZERO_SLICING = config['ZERO_SLICING']
ONE_SLICING = config['ONE_SLICING']
TEAMS_NAME = config['TEAMS_NAME']
PATTERN = config['PATTERN']
PREDICTIONS = config['PREDICTIONS']
HOME_PROBABILITY = config['HOME_PROBABILITY']
AWAY_PROBABILITY = config['AWAY_PROBABILITY']
DRAW_PROBABILITY = config['DRAW_PROBABILITY']
PAGINATION = config['PAGINATION']
NEXT_PAGE = config['NEXT_PAGE']

logger = logging.getLogger('flashscore')


def fetch_fixtures_predictions():
    """
    retrieves predections for future fixtures on the next 20 days.
    :return: list of lists, where each list represents one future fixture, with the names of the participating teams and
    match results probabilities.
    """
    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=DAYS)
    data_query_api = f'https://api.sportmonks.com/v3/football/fixtures/between/{current_date}/{end_date}?api_token=oi64fLLyqqwd2biIQtrFTCvh4YP7lPMNawZRUOxBFkk16Afy8e22RSdN7FVO&include=predictions&filters=fixtureLeagues:8;predictionTypes:237'
    predictions_list = []
    while True:
        response = requests.get(data_query_api)
        if response.status_code == RESPONSE_STATUS_CODE:
            response_dict = response.json()
            response_data = response_dict[RESPONSE_DATA_LIST]
            for data in response_data:
                single_fixture_prediction = []
                match_pattern = [(match.start(), match.end()) for match in re.finditer(PATTERN, data[TEAMS_NAME])]
                single_fixture_prediction.append(
                    data[TEAMS_NAME][ZERO_SLICING:match_pattern[ZERO_SLICING][ZERO_SLICING]])
                single_fixture_prediction.append(data[TEAMS_NAME][match_pattern[ZERO_SLICING][ONE_SLICING]::])
                single_fixture_prediction.append(data[PREDICTIONS][ZERO_SLICING][PREDICTIONS][HOME_PROBABILITY])
                single_fixture_prediction.append(data[PREDICTIONS][ZERO_SLICING][PREDICTIONS][DRAW_PROBABILITY])
                single_fixture_prediction.append(data[PREDICTIONS][ZERO_SLICING][PREDICTIONS][AWAY_PROBABILITY])
                predictions_list.append(single_fixture_prediction)
        else:
            logger.error(
                f'CRITICAL: Access to webpage denied! No response from webpage.\nStatus code: {response.status_code}')
        next_page = response_dict[PAGINATION][NEXT_PAGE]
        if next_page is not None:
            token_index = next_page.find('?')
            data_query_api = next_page[
                             ZERO_SLICING:token_index + ONE_SLICING] + 'api_token=oi64fLLyqqwd2biIQtrFTCvh4YP7lPMNawZRUOxBFkk16Afy8e22RSdN7FVO&' + next_page[
                                                                                                                                                   token_index + ONE_SLICING::]
        else:
            logger.info('Scrapped future fixtures odds and predictions information successfully')
            return predictions_list
