import re
BOWLERS = [
    "Akash Madhwal",
    "Mohammad Siraj",
    "Mustafizur Rahman",
    "Yash Dayal",
    "Mitchell Starc",
    "Mukesh Choudhary",
    "Trent Boult",
    "Harshal Patel",
    "Ravi Bishnoi",
    "Kuldeep Yadav",
    "Bhuvneshwar Kumar",
    "Deepak Chahar",
    "Yuzvendra Chahal",
    "Arshdeep Singh",
    "Mujeeb Ur Rahman",
    "Pat Cummins"
]


def process_string(input_string):
    # Replace characters other than a-z, A-Z, and / with a space
    processed_string = re.sub(r'[^a-zA-Z/]', ' ', input_string)
    
    # Replace multiple spaces with a single space
    processed_string = re.sub(r'\s+', ' ', processed_string).strip()
    
    # Split the processed string based on spaces and /
    result = [word for word in re.split(r'[ /]', processed_string) if word]
    
    return result

def findPlayer(playerTakenWicket, batsmanTeam, playerStats):

    for playerStat in playerStats:
        if(playerStat['Team'] != batsmanTeam):
            playerName = playerStat['Player Name']

            if(playerName.lower() == playerTakenWicket.lower()):

                return playerName
            
            playerName = playerName.split()

            if(playerTakenWicket.lower() == playerName[-1].lower()):
                return playerStat['Player Name']
            
            if playerTakenWicket in playerStat['Player Name']:
                return playerStat['Player Name']

    return ""



def findPlayerInHowOutAndUpdatePoints(how_out,pos,playerPoints,playerStat,playerStats,points):
    
    playerTakenWicket = ""
    playerTakenWicket += how_out[pos]

    for element in how_out[pos+1:]:
        if(element == 'b'):
            break
        else:
            playerTakenWicket+=" "
            playerTakenWicket+= element

    playerTakenWicket = findPlayer(playerTakenWicket,playerStat['Team'], playerStats)

    if(len(playerTakenWicket) >0):
        playerPoints[playerTakenWicket] = playerPoints.get(playerTakenWicket,0) + points


    return playerPoints


'''
Note : Not Applicable for bowlers 
1 point per run
1 point per boundary bonus
2 points per six scored
4 points for scoring 30 runs
8 points for a half-century
16 points for a century
-2 points if dismissed for a duck (Only for batsmen, wicket-keepers, and all-rounders)

'''

def is_float_try_except(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def calculateBattingPoints(team_players_dict,playerStat,playerStats,playerPoints):
    points = 0
    runs = int(playerStat['Runs'])
    
    if(is_float_try_except(playerStat['Strike Rate'])):
        strikeRate = float(playerStat['Strike Rate'])

    ballsPlayed = int(playerStat['Balls'])
    how_out = process_string(playerStat['how_out'])

    points += runs
    points += int(playerStat['Fours'])
    points += (2*int(playerStat['Sixes']))

    if runs >=100:
        points += 16
    elif runs >=50:
        points +=8
    elif runs >=30:
        points += 4

    if(not isBowler(team_players_dict,playerStat)):

        if (runs == 0):
            points -=2
        
        if ( ballsPlayed >= 10):

            if(strikeRate >170):
                points +=6
            elif(strikeRate >150 and strikeRate <170):
                points +=4
            elif(strikeRate >=130 and strikeRate <=150):
                points +=2
            elif(strikeRate >=60 and strikeRate <=70):
                points -=2
            elif(strikeRate >=50 and strikeRate <=59.99):
                points-=4
            elif( strikeRate < 50):
                points-=6
   
    playerName = playerStat['Player Name']
    playerPoints[playerName] = playerPoints.get(playerName, 0) + points

    
    return playerPoints


#calculate bowling points
'''
25 points per wicket, excluding run-outs
8 bonus points for taking the wicket by LBW or Bowled
4 bonus points for taking three wickets in a single match
8 bonus points for taking four wickets in a single match
16 bonus points for taking five wickets in a single match
12 points per maiden over

----Economy Rate Points (Min 2 Overs To Be Bowled)-----

6 points if his economy rate is below 5 runs per over
4 points if his economy rate is between 5 - 5.99 runs per over
2 points if his economy rate is between 6 - 7 runs per over
-2 points if his economy rate is between 10 - 11 runs per over
-4 points if his economy rate is between 11.01 - 12 runs per over
-6 points if his economy rate is above 12 runs per over
'''

def isBowler(team_players_dict,playerStat):

    if playerStat['Player Name'].lower() in [name.lower() for name in BOWLERS]:
        return 1
    
    return 0

def calculateBowlingPoints(team_players_dict,playerStat,playerPoints):

    points =0
    wickets = int(playerStat['wickets'])
    points += (25*wickets)
    if(is_float_try_except(playerStat['economy'])):
        economy = float(playerStat['economy'])

    if(wickets>=5):
        points +=16
    elif(wickets>=4):
        points +=8
    elif(wickets>=3):
        points+=4
    
    points += (12*int(playerStat['maiden']))

    if(playerStat['overs'][0]>='2'):

        if(economy >12):
            points -=6
        elif(economy<=12 and economy >=11.1):
            points -=4
        elif(economy<=11 and economy >=10):
            points -=2
        elif(economy<=7 and economy >=6):
            points +=2
        elif(economy<6 and economy >=5):
            points +=4
        elif(economy<5):
            points +=6
        
    playerName = playerStat['Player Name']
    playerPoints[playerName] = playerPoints.get(playerName, 0) + points

    return playerPoints
    

#fielding points 
'''
8 points per catch
4 bonus points for taking three catches in one match
12 points per stump/direct run-out
6 points per throw leading to a run-out
6 points per catch leading to a run-out
'''

def lastName(playerName):
    lastName = ""
    for i in range(len(playerName)-1,0,-1):
        if(playerName[i] == ' '):
            break
        else:
            lastName+=playerName[i]
    lastName[::-1]
    return lastName
    # print(lastName)

def getTeam(player,playerStats):

    for playerStat in playerStats:
        if(playerStat['Player Name'].lower() == player.lower()):
            return playerStat['Team']


def calculateWicketPoints(team_players_dict,playerStat,playerStats,playerPoints,TEAMS):
    how_out = process_string(playerStat['how_out'])
    
    if(how_out[0][0]=='l' or how_out[0][0]=='b'):
        if how_out[0][0]=='l':
            if(how_out[2]=='sub'):
                playerPoints = findPlayerInHowOutAndUpdatePoints(how_out,3,playerPoints,playerStat,playerStats,8)
            else:
                playerPoints = findPlayerInHowOutAndUpdatePoints(how_out,2,playerPoints,playerStat,playerStats,8)
        else:
            if(how_out[1]=='sub'):
                playerPoints = findPlayerInHowOutAndUpdatePoints(how_out,2,playerPoints,playerStat,playerStats,8)
            else:
                playerPoints = findPlayerInHowOutAndUpdatePoints(how_out,1,playerPoints,playerStat,playerStats,8)

    elif(how_out[0][0]=='s'):
        if(how_out[1]=='sub'):
            playerPoints = findPlayerInHowOutAndUpdatePoints(how_out,2,playerPoints,playerStat,playerStats,12)
        else :
            playerPoints = findPlayerInHowOutAndUpdatePoints(how_out,1,playerPoints,playerStat,playerStats,12)
    elif(how_out[0][0]=='c'):
        
        if(how_out[1]=='amp'):
            if(how_out[3]=='sub'):
                playerPoints = findPlayerInHowOutAndUpdatePoints(how_out,4,playerPoints,playerStat,playerStats,8)
            else:
                playerPoints = findPlayerInHowOutAndUpdatePoints(how_out,3,playerPoints,playerStat,playerStats,8)
        else:
            if(how_out[1]=='sub'):
                playerPoints = findPlayerInHowOutAndUpdatePoints(how_out,2,playerPoints,playerStat,playerStats,8)
            else:
                playerPoints = findPlayerInHowOutAndUpdatePoints(how_out,1,playerPoints,playerStat,playerStats,8)

    elif(how_out[0][0] == 'r' and isPlayerPresentInDic(team_players_dict, playerStat,TEAMS)):
        print()
        print("run out points are not calculate yet but will soon be calulated : ", how_out)
        print()
        
    return playerPoints

def isPlayerPresentInDic(team_players_dict, playerStat,TEAMS):
    for team in TEAMS:
        for index, player_data in team_players_dict[team].items():
            if(index == 'total_points'):
                break
            playerName = player_data['name']
            if playerName == playerStat['Player Name']:
                return 1
    return 0


def updatePointsOfPlayers(team_players_dict,playerStats,TEAMS):
    playerPoints = {}
    for playerStat in playerStats:

        if(isPlayerPresentInDic(team_players_dict, playerStat,TEAMS)):
            if(playerStat['Type'] == 'Batting'):
                # print('Bat',playerStat['Player Name'])
                # print(playerStat)
                playerPoints = calculateBattingPoints(team_players_dict, playerStat,playerStats, playerPoints)
                # print(playerPoints)
                # print()
            elif(playerStat['Type'] == 'Not Batted'):
                # print('Not Batted',playerStat['Player Name'])
                # print(playerStat)
                playerPoints[playerStat['Player Name']] = playerPoints.get(playerStat['Player Name'],0)
                # print(playerPoints)
                # print()
            elif(playerStat['Type'] == 'Bowling'):
                # print('Bowl',playerStat['Player Name'])
                # print(playerStat)
                playerPoints = calculateBowlingPoints(team_players_dict, playerStat, playerPoints)
                # print(playerPoints)
                # print()

    for playerStat in playerStats:

        if(playerStat['Type'] == 'Batting'):
            # print('out',playerStat['Player Name'])
            # print(playerStat)
            playerPoints = calculateWicketPoints(team_players_dict,playerStat, playerStats, playerPoints,TEAMS)
            # print(playerPoints)
            # print()


    for player in playerPoints:
        playerPoints[player]+=4
    
    # print(playerPoints)
    for team in TEAMS:
        for index, player_data in team_players_dict[team].items():
            if(index == 'total_points'):
                break
            playerName = player_data['name']
            if playerName in playerPoints:
                team_players_dict[team][index]['points'] = team_players_dict[team][index].get('points',0) + playerPoints[playerName]

    # print()
    # print(playerPoints)
    # print()
    
    
    return team_players_dict



