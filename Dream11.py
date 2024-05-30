import os.path
import sys
import json
import time
import shutil
sys.path.append('/Users/akshitagarwal/opt/anaconda3/lib/python3.9/site-packages')

import gspread
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from DataExtraction import *
from PointsCalculation import *

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1ELK7fdAPnJgBierAGGF3vl2jWhpFUGfnfeeD4z-o-48'
SHEET_INDEX = 2
TEAMS = ["AATESH", "HEET", "PRATEEK", "RACHIT", "YASH"]

team_players_dict = {
    "AATESH": {
        0: {'name': 'Shikhar Dhawan', 'player_id': 84717, 'type': None, 'points': 0},
        1: {'name': 'Shubman Gill', 'player_id': 3210531, 'type': None, 'points': 0},
        2: {'name': 'Sai Sudharsan', 'player_id': 3453876, 'type': None, 'points': 0},
        3: {'name': 'Jitesh Sharma', 'player_id': 2165613, 'type': None, 'points': 0},
        4: {'name': 'Venkatesh Iyer', 'player_id': 2554221, 'type': None, 'points': 0},
        5: {'name': 'Glenn Maxwell', 'player_id': 975090, 'type': None, 'points': 0},
        6: {'name': 'Cameron Green', 'player_id': 3230151, 'type': None, 'points': 0},
        7: {'name': 'Andre Russell', 'player_id': 828906, 'type': None, 'points': 0},
        8: {'name': 'Ravindra Jadeja', 'player_id': 704037, 'type': None, 'points': 0},
        9: {'name': 'Mustafizur Rahman', 'player_id': 992718, 'type': None, 'points': 0},
        10: {'name': 'Yuzvendra Chahal', 'player_id': 1290750, 'type': None, 'points': 0},
        11: {'name': 'Devdutt Padikkal', 'player_id': 3357090, 'type': None, 'points': 0}
    },
    "HEET": {
        0: {'name': 'Rohit Sharma', 'player_id': 102318, 'type': None, 'points': 0},
        1: {'name': 'Jos Buttler', 'player_id': 926913, 'type': None, 'points': 0},
        2: {'name': 'Quinton de Kock', 'player_id': 1137441, 'type': None, 'points': 0},
        3: {'name': 'KL Rahul', 'player_id': 1266336, 'type': None, 'points': 0},
        4: {'name': 'Kane Williamson', 'player_id': None, 'type': None, 'points': 0},
        5: {'name': 'Rahmanullah Gurbaz', 'player_id': None, 'type': None, 'points': 0},
        6: {'name': 'Trent Boult', 'player_id': 833748, 'type': None, 'points': 0},
        7: {'name': 'Akash Madhwal', 'player_id': None, 'type': None, 'points': 0},
        8: {'name': 'Yash Dayal', 'player_id': 3479172, 'type': None, 'points': 0},
        9: {'name': 'Jasprit Bumrah', 'player_id': 1876161, 'type': 'Bowler', 'points': 0},
        10: {'name': 'Bhuvneshwar Kumar', 'player_id': 978060, 'type': None, 'points': 0},
        11: {'name': 'Abhishek Sharma', 'player_id': 3210561, 'type': None, 'points': 0}
    },
    "PRATEEK": {
        0: {'name': 'Ruturaj Gaikwad', 'player_id': 3181152, 'type': None, 'points': 0},
        1: {'name': 'Faf du Plessis', 'player_id': 134496, 'type': None, 'points': 0},
        2: {'name': 'Yashasvi Jaiswal', 'player_id': 3453846, 'type': None, 'points': 0},
        3: {'name': 'Rishabh Pant', 'player_id': 2794755, 'type': None, 'points': 0},
        4: {'name': 'Daryl Mitchell', 'player_id': 1145241, 'type': None, 'points': 0},
        5: {'name': 'Deepak Hooda', 'player_id': 1491375, 'type': None, 'points': 0},
        6: {'name': 'Shivam Dube', 'player_id': 2143365, 'type': None, 'points': 0},
        7: {'name': 'Wanindu Hasaranga', 'player_id': None, 'type': None, 'points': 0},
        8: {'name': 'Axar Patel', 'player_id': 1664085, 'type': None, 'points': 0},
        9: {'name': 'Deepak Chahar', 'player_id': 1341795, 'type': None, 'points': 0},
        10: {'name': 'Pat Cummins', 'player_id': 1469679, 'type': None, 'points': 0},
        11: {'name': 'Ravi Bishnoi', 'player_id': 3526335, 'type': None, 'points': 0}
    },
    "RACHIT": {
        0: {'name': 'David Warner', 'player_id': 659679, 'type': None, 'points': 0},
        1: {'name': 'Virat Kohli', 'player_id': 761418, 'type': None, 'points': 0},
        2: {'name': 'Shreyas Iyer', 'player_id': 1927569, 'type': None, 'points': 0},
        3: {'name': 'Sanju Samson', 'player_id': 1277841, 'type': None, 'points': 0},
        4: {'name': 'Mitchell Marsh', 'player_id': 817362, 'type': None, 'points': 0},
        5: {'name': 'Krunal Pandya', 'player_id': 1414038, 'type': None, 'points': 0},
        6: {'name': 'Sunil Narine', 'player_id': 691686, 'type': None, 'points': 0},
        7: {'name': 'Mitchell Starc', 'player_id': 934788, 'type': None, 'points': 0},
        8: {'name': 'Arshdeep Singh', 'player_id': 3377940, 'type': None, 'points': 0},
        9: {'name': 'Mohammed Siraj', 'player_id': 2822931, 'type': None, 'points': 0},
        10: {'name': 'Harshal Patel', 'player_id': 1171455, 'type': None, 'points': 0},
        11: {'name': 'Mayank Agarwal', 'player_id': 1195326, 'type': None, 'points': 0}
    },
    "YASH": {
        0: {'name': 'Tilak Varma', 'player_id': 3510807, 'type': None, 'points': 0},
        1: {'name': 'Travis Head', 'player_id': 1590045, 'type': None, 'points': 0},
        2: {'name': 'Ishan Kishan', 'player_id': 2161425, 'type': None, 'points': 0},
        3: {'name': 'Suryakumar Yadav', 'player_id': None, 'type': None, 'points': 0},
        4: {'name': 'Rashid Khan', 'player_id': 2380401, 'type': None, 'points': 0},
        5: {'name': 'Kyle Mayers', 'player_id': None, 'type': None, 'points': 0},
        6: {'name': 'Hardik Pandya', 'player_id': 1876125, 'type': None, 'points': 0},
        7: {'name': 'Rachin Ravindra', 'player_id': 2879313, 'type': None, 'points': 0},
        8: {'name': 'Mukesh Choudhary', 'player_id': None, 'type': None, 'points': 0},
        9: {'name': 'Kuldeep Yadav', 'player_id': 1677717, 'type': None, 'points': 0},
        10: {'name': 'Dhruv Jurel', 'player_id': 3526476, 'type': None, 'points': 0},
        11: {'name': 'Rinku Singh', 'player_id': 2169327, 'type': None, 'points': 0}
    }
}

def backupFile(fileName):   
    source_file = open(fileName, 'rb')
    fileName += ".backup"
    dest_file = open(fileName, 'wb')
    shutil.copyfileobj(source_file, dest_file)



def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', SCOPES)
    client = gspread.authorize(creds)

    # Open the spreadsheet by its title
    spreadsheet = client.open_by_key(SPREADSHEET_ID)

    # Select the specified sheet
    sheet = spreadsheet.get_worksheet(SHEET_INDEX)

    team_players_dict = {}
    matchesStats = {}
    nextMatchToProcess = 0
    result = []


    with open('ipl_matches_list.json', 'r') as f:
        matches = json.load(f)
    
    with open('team_players_data.json', 'r') as f:
        team_players_dict = json.load(f)

    with open('next_match_to_Process.txt', 'r') as f:
        nextMatchToProcess = int(f.read().strip()) 

    with open('matches_stats.json', 'r') as f:
        matchesStats = json.load(f)

    while(1):

        nextMatchToProcessDetails = getMatchDetails(matches, nextMatchToProcess)
        
        playerStats = getMatchPlayersStats(nextMatchToProcessDetails['Match Id'])
        print(playerStats)
        if(playerStats):
            team_players_dict = updatePointsOfPlayers(team_players_dict, playerStats, TEAMS)
            
            matchesStats[nextMatchToProcess] = playerStats

            nextMatchToProcess = nextMatchToProcess + 1
            print(playerStats)
        else:
            print("calculating points started")
                #Calculate and update total points for each team
            for team, players in team_players_dict.items():
                min_score = 1000000
                total_points = sum(players[str(i)]['points'] for i in range(0,12))
                for i in range(0,12):
                    min_score = min(min_score,int(players[str(i)]['points']))
                total_points = total_points - min_score
                team_players_dict[team]['total_points'] = total_points
                result.append('Total Pts(Top 11)')
                result.append(total_points)

            #Format the data
            headers = ["\t".join([f"{team}\tPoints" for team in team_players_dict.keys()])]
            data = []

            for i in range(12):  # Assuming each team has 12 players
                row_data = []
                for team, players in team_players_dict.items():
                    player = list(players.values())[i]
                    row_data.extend([player['name'], str(player['points'])])
                data.append("\t".join(row_data))
            

            headers = ["\t".join([f"{team}\tPoints" for team in team_players_dict.keys()])]
            header_value = headers[0]
            header_cells = header_value.split("\t")
            for idx, cell_value in enumerate(header_cells, start=1):
                sheet.update_cell(1, idx, cell_value)

            data_rows = [row_data.split("\t") for row_data in data]


            print("calculating points ended")
            print("writing data in sheet started")
            for idx, row_data in enumerate(data_rows, start=2):
                sheet.update(f"A{idx}:J{idx}", [row_data])

            sheet.update(f"A14:J14",[result])

            updatedTill = [
                "Score Update Till match :",
                matches[nextMatchToProcess-2]['Home Team'],
                matches[nextMatchToProcess-2]['Away Team'],
            ]
            sheet.update(f"A18:C18",  [updatedTill ])

            sheet.update(f"A19:B19",[["matchNo",matches[nextMatchToProcess-2]['Match Number']]])
            print("writing data in sheet ended")

            print("Backup Started")
            backupFile('team_players_data.json')
            backupFile('next_match_to_Process.txt')
            backupFile('matches_stats.json')
            print("Backup Ended")
            print("file updation started")
            with open('team_players_data.json', 'w') as f:
                json.dump(team_players_dict,f)

            with open('next_match_to_Process.txt', 'w') as f:
                f.write(str(nextMatchToProcess))

            with open('matches_stats.json', 'w') as f:
                json.dump(matchesStats,f)
            print("file updation ended")
            return
if __name__ == "__main__":
    main()
