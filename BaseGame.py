import token
from pprint import pprint
from random import randint

import requests
import json
import hashlib

payload = {'GameURL': 'https://develop-games.api.perfecttlos.com/',
           'FrontURL': 'https://redirector-develop.perfecttlos.com/',
           'PartnerURL': 'https://develop-partner.perfecttlos.com/',
           'partnerId': '360',
           'currency': 'USD',
           'gameId': '14001',
           'userID': randint(100, 105)}

request = requests.get('https://testpartnerservice.perfecttlos.com/setup', params=payload)
# print(request.text) ## тут мы получили токен

t = request.text
regToken = t.split("token=")[1].split("&")[0]
# print(gametoken) ## Тут мы забрали токен

############################################## AuthorizationGame ################################################

HASHauth = hashlib.md5(('AuthorizationGame/' + regToken + 'TestKey').encode()).hexdigest()
# print(HASHauth)

response = requests.post('https://develop-games.api.perfecttlos.com/auth/AuthorizationGame/',
                         json={'Hash': HASHauth, 'Token': regToken},
                         verify=False)
# pprint(response.json())

################################################# GetSlotInfo ###############################################

hashslot = hashlib.md5(('GetSlotInfo/' + regToken + 'TestKey').encode()).hexdigest()
# print(hashslot)

response = requests.post('https://develop-games.api.perfecttlos.com/games/GetSlotInfo',
                         json={'Hash': hashslot, 'Token': regToken},
                         verify=False)
# pprint(response.json())

################################################### CreditDebit ###############################################

http = 'https://develop-games.api.perfecttlos.com/games/CreditDebit'
BetSum = '6'
CntLineBet = '10'
GameKey = 'TestKey'


def CreditDebit(**data):
    HASH = hashlib.md5(('CreditDebit/' + data['regToken'] + data['betSum'] + data['cntLineBet'] + data[
        'gamekey']).encode()).hexdigest()
    params = {'Hash': HASH, 'Token': data['regToken'], 'BetSum': data['betSum'], 'CntLineBet': data['cntLineBet']}
    response = requests.post(http, json=params, verify=False)
    response = response.json()
    return response, response['TokenAsync'], response['Timeout']

# creditDebit, tokenAsync, timeout = CreditDebit(regToken=regToken, betSum=BetSum, cntLineBet=CntLineBet, gamekey=GameKey)



#################################################### GetAsyncResponce ##################################################

def GetAsyncResponse(regToken, tokenAsync, gamekey):
    HASH = hashlib.md5(('GetAsyncResponse/' + tokenAsync + gamekey).encode()).hexdigest()
    params = {'Hash': HASH, 'Token': regToken, 'TokenAsync': tokenAsync}
    response = requests.post('https://develop-games.api.perfecttlos.com/games/GetAsyncResponse', json=params, verify=False)
    response = response.json()
    while 'Error' in response:
        response = requests.post('https://develop-games.api.perfecttlos.com/games/GetAsyncResponse', json=params,
                                 verify=False)
        response = response.json()
    return response

# pprint(GetAsyncResponse(regToken=regToken, tokenAsync=tokenAsync, gamekey=GameKey))

rounds = 5
i = 0
while i < rounds:
    creditDebit, tokenAsync, timeout = CreditDebit(regToken=regToken, betSum=BetSum, cntLineBet=CntLineBet,
                                                   gamekey=GameKey)
    GetAsyncResponse(regToken=regToken, tokenAsync=tokenAsync, gamekey=GameKey)
    i = i+1
    print(i)