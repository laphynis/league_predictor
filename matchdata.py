from riotwatcher import LolWatcher, ApiError
import roleml
import requests, json
import time
#from oauth2client.service_account import ServiceAccountCredentials
#import gspread

# initialize connection to Riot API
api = 'RGAPI-43dd3c41-2ca8-4df8-bb42-de98f63a75ea'
watcher = LolWatcher(api)

# read the json that contains thousands of match ids
url = 'https://canisback.com/matchId/matchlist_na1.json'
data = json.loads(requests.get(url).text)

# intialize the connection to google sheets
#scope = ['https://spreadsheets.google.com/feeds',
#         'https://www.googleapis.com/auth/spreadsheets',
#         'https://www.googleapis.com/auth/drive.file',
#         'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
#client = gspread.authorize(creds)

#sheet = client.open('League Matches').sheet1

role_order = {'top' : 1, 'jungle': 2, 'mid': 3, 'bot': 4, 'supp': 5}

for match in data:
    try:
        match_details = watcher.match.by_id('na1', match)
        if match_details['queueId'] in [420, 421, 422]:
            
            file = open('data.csv', 'a+')
            timeframes = watcher.match.timeline_by_match('na1', match)
            role_dict = roleml.predict(match_details, timeframes)
            
            list_of_participants = []
            organized_list = []
            
            for p in match_details['participants']:
                role = role_dict[p['participantId']]
                champion = p['championId']
                summ1 = p['spell1Id']
                summ2 = p['spell2Id']
                keystone = p['stats']['perk0']
                xpDiff = p['timeline']['xpPerMinDeltas']['0-10']
                goldDiff = p['timeline']['goldPerMinDeltas']['0-10']
                list_of_participants.append((p['participantId'], role,
                                             champion, summ1, summ2,
                                             keystone, xpDiff, goldDiff))
            
            list_of_participants = sorted(list_of_participants,
                                          key=lambda x: role_order[x[1]])
            for p in list_of_participants:
                for d in p[2: ]:
                    d = str(d)
                    organized_list.append(d)
            
            string = ','.join(organized_list)
            file.write('\n' + string)
            #sheet.insert_row(organized_list, 3)
            
            file.close()

    except Exception:
        print('Exception occurred')
        continue

    finally:
        # wait 2 seconds before continuing to fit the 200 requests per minute limit
        time.sleep(1)

print('Finished!')
