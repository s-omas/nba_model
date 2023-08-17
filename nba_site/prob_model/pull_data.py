import requests


def get_teams():
    url = "https://api-nba-v1.p.rapidapi.com/standings"
    querystring = {"league":"standard","season":"2022"}
    with open('./key.txt', 'r') as file:
        k = file.read()

    headers = {
        "X-RapidAPI-Key": k,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    res = response.json()['response']
    teams = [x['team']['name'] for x in res]
    return teams