import requests


def calculateRangeToProcess(col):
    global RANGE_NAME
    RANGE_NAME = "Standing!" + chr(65 + col - 1) + '2' + ':' + chr(65 + col - 1) + "13"

def getPlayersNames():
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    return values

def getIPLSeriesData():
    url = "https://cricket-live-data.p.rapidapi.com/fixtures-by-series/2002"

    headers = {
        "X-RapidAPI-Key": "d2839aae95mshb725fbf399ecc98p148f73jsne301fdc91c7f",
        "X-RapidAPI-Host": "cricket-live-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response.json()


def getIPLMatchesList():
    matches = []
    data = getIPLSeriesData()


    for match in data['results']:
        match_details = {
            'Match Id': match['id'],
            'Match Number': match['match_subtitle'],
            'Venue': match['venue'],
            'Date': match['date'],
            'Status': match['status'],
            'Result': match['result'],
            'Home Team': match['home']['name'],
            'Away Team': match['away']['name'],
            'Winner': match['result'].split(' ')[0] if 'won' in match['result'] else 'No Result'
        }
        if(match_details['Match Number'][1]>='0' and match_details['Match Number'][1]<='9'):
            match_details['Match Number'] = match_details['Match Number'][:2]
        elif(match_details['Match Number'][0]>='0' and match_details['Match Number'][0]<='9'):
            match_details['Match Number'] = match_details['Match Number'][:1]

        matches.append(match_details)

    # for match in matches:
    #     print(match)

    return matches

def getMatchStats(matchId):

    url = "https://cricket-live-data.p.rapidapi.com/match/" + str(matchId)

    headers = {
       "X-RapidAPI-Key": "d2839aae95mshb725fbf399ecc98p148f73jsne301fdc91c7f",
       "X-RapidAPI-Host": "cricket-live-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    return response.json()


def getMatchPlayersStats(matchId):
    
    data = getMatchStats(matchId)
    print(data)
    if(data['results']['live_details'] and data['results']['live_details']['match_summary']['result']=='No'):
        return None
    if(data['results']['live_details'] == None):
        return None

    player_stats = []
    
    scorecard = data['results']['live_details']['scorecard']
    for inning in scorecard:

        for player in inning['batting']:
            stats = {
            'Type': "Batting",
            'Team': inning['title'],
            'Player Name': player['player_name'],
            'Player Id' : player['player_id'],
            'Runs': player['runs'],
            'Balls': player['balls'],
            'Fours': player['fours'],
            'Sixes': player['sixes'],
            'Strike Rate': player['strike_rate'],
            'how_out' : player['how_out']
             }
            player_stats.append(stats)

        for player in inning['still_to_bat']:
            stats = {
            'Type': "Not Batted",
            'Team': inning['title'],
            'Player Name': player['player_name'],
            'Player Id' : player['player_id']
            }
            player_stats.append(stats)

        for player in inning['bowling']:
            stats = {
            'Type': "Bowling",
            'Team': inning['title'],
            'Player Id': player['player_id'],
            'Player Name': player['player_name'],
            'overs' : player['overs'],
            'maiden': player['maidens'],
            'runs' : player['runs_conceded'],
            'wickets': player['wickets'],
            'economy': player['economy'],
            'dot_balls': player['dot_balls'],
            'fours': player['fours'],
            'sixes': player['sixes'],
            'extras': player['extras']
            }
            player_stats.append(stats)

# Print player stats
    # for stats in player_stats:
    #     print(stats)
            
    return player_stats

def getMatchDetails(matches, matchNo):
    if(matchNo>len(matches)):
        print("match no is out of range !!")
        return -1
    match = matches[matchNo-1]

    if(int(match['Match Number']) == matchNo ):
        return  match
    else: 
        print("mismatched match no !!")
        return -1

def checkAndUpdateIdInDic(player_stat,team_players_dict,TEAMS):
    for team in TEAMS:
        for i in range(0,12):
            if(team_players_dict[team][i]['name'].lower() == player_stat['Player Name'].lower() and team_players_dict[team][i]['player_id'] == None  ):
                team_players_dict[team][i]['player_id'] = player_stat['Player Id']

    return team_players_dict



def mapPlayerNameToPlayerId(team_players_dict,TEAMS):
    matches = getIPLMatchesList()
    for i in range (0,10):
        match = matches[i]
        player_stats = getMatchPlayersStats(match['Match Id'])

        




    


