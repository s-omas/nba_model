import requests
import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "key.txt")
with open(file_path, 'r') as file:
    k = file.read()
    k = k.decode('utf-8').strip()


def api_get(url, querystring):
    try:
        headers = {
            "X-RapidAPI-Key": k,
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        return response
    except:
        print("trying proxy")
        proxies = {
            'https': 'proxy.server:3128'
            }
        response = requests.post(url, headers=headers, params=querystring, proxies=proxies)
        return response


def api_get_standings(season):
    url = "https://api-nba-v1.p.rapidapi.com/standings"
    querystring = {"season":season}
    data = api_get(url, querystring)
    return data.json()

def api_get_games(season):
    url = "https://api-nba-v1.p.rapidapi.com/games"
    querystring = {"season":season}
    data = api_get(url, querystring)
    return data.json()

def api_get_games_on_date(date):
    url = "https://api-nba-v1.p.rapidapi.com/games"
    querystring = {"date":date}
    data = api_get(url, querystring)
    return data.json()


# def api_get(request_string):
#     #try without proxy (for local development)
#     try:
#         conn = http.client.HTTPSConnection("api-nba-v1.p.rapidapi.com")
#         headers = {
#             'X-RapidAPI-Key': k,
#             'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com"
#         }
#         conn.request("GET", request_string, headers=headers)
#         res = conn.getresponse()
#         data = res.read()
#         return data
#     except:
#         print("trying proxy")
#         # Proxy configuration
#         proxy_host = 'proxy.server'
#         proxy_port = 3128  # Replace with your proxy server's port
#         proxy_tunnel = False  # Set to True if your proxy uses tunneling, else False

#         # Create a connection to the proxy server
#         conn = http.client.HTTPConnection(proxy_host, proxy_port, timeout=10)
#         endpoint = "api-nba-v1.p.rapidapi.com"

#         # Establish a connection to the target server through the proxy
#         if proxy_tunnel:
#             conn.set_tunnel(endpoint, 443)  # Replace with your target server's hostname and port
#         else:
#             conn.request("GET", request_string)

#         # Add headers, including those for the proxy
#         headers = {
#             'X-RapidAPI-Key': k,
#             'X-RapidAPI-Host': "api-nba-v1.p.rapidapi.com",
#         }

#         for key, value in headers.items():
#             conn.putheader(key, value)

#         conn.endheaders()

#         # Get the response from the target server through the proxy
#         res = conn.getresponse()
#         data = res.read()
#         return data
    

# def api_get_standings(season):
#     data = api_get("/standings?league=standard&season=" + season)
#     return json.loads(data.decode("utf-8"))

# def api_get_games(season):
#     data = api_get("/games?season=" + season)
#     return json.loads(data.decode("utf-8"))

# def api_get_games_on_date(date):
#     data = api_get("/games?date=" + date)
#     return json.loads(data.decode("utf-8"))