"""
This file contains util functions that perform API calls
"""
import json
import sys

import requests

API_KEY="RRU3luwDGuknU0Sy16iUXX52G7qCeDnU"
API_SECRET="ASSQQlF8qWj5Vt3F"

def get_access_token():
    base_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    params = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": API_SECRET
    }

    response = requests.request("POST", base_url, headers=headers, data=params)
    access_token = json.loads(response.text)["access_token"]
    return access_token

def get_airport_info(parameters):
    '''
    gets related airport information based on keyword
    the keyword is going to be part of a city name
    ex. if given new as keyword, the API may return airports located in New York

    :param keyword: a query parameter for the airport search
    :return data: response data in dictionary format
    '''
    # get access token
    access_token = get_access_token()
    base_url = "https://test.api.amadeus.com/v1/reference-data/locations"
    headers = {
        'Authorization': 'Bearer ' + str(access_token)
    }
    data = {}
    status = ""
    try:
        response = requests.get(base_url, params=parameters, headers=headers)
        # print(response)
        data = json.loads(response.text)
        status = "success"
    except requests.exceptions.HTTPError as err:
        status = "fail"
    return data, status

def get_ticket_info(parameters):
    ''' 
    fetches ticket options based on the input parameters

    :param parameters: a dictionary containing all query parameters
    :return data: response data in dictionary format
    '''

    access_token = get_access_token()
    base_url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    headers = {
        'Authorization': 'Bearer ' + str(access_token)
    }
    data = {}
    status = ""
    try:
        response = requests.get(base_url, headers=headers, params=parameters)
        data = json.loads(response.text)
        status = "success"
    except requests.exceptions.HTTPError as err:
        status = "fail"
    return data, status


# def test():
#     parameters = {
#         "keyword": "new",
#         "subType": "AIRPORT"
#     }
#     resp, stat = get_airport_info(parameters)
#     print(resp)
#     print(stat)
#     # parameters = {
#     #     "originLocationCode": "BOS",
#     #     "destinationLocationCode": "JFK",
#     #     "departureDate": "2022-11-07",
#     #     "adults": 1
#     # }
#     # resp = get_ticket_info(parameters)

# if __name__ == "__main__":
#     test()
