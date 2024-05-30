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
SPREADSHEET_ID = '1RBrocGFbBRYN9xMWt285_M2Subf-Ylzz8ow3tOFsgiQ'
SHEET_INDEX = 0


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

    data = [
    ['Minakshi'], ['Meera'], ['Sarita'], ['Pooja'], ['Sita'], ['Manisha'], ['Sima'], ['Sunita'], ['Asha'], ['Jyoti'],
    ['Kamla'], ['Sama'], ['Saroj'], ['Anu'], ['Priya'], ['Lakhshmi'], ['Mukesh'], ['Ati'], ['Nisha'], ['Priti'], ['Mamta'],
    ['Suman'], ['Sunita'], ['Manisha'], ['Alka'], ['Raju'], ['Minakshi'], ['Priti'], ['Mona'], ['Priya'], ['Triveni'],
    ['Shiva'], ['Tom'], ['Sunita'], ['Mamta'], ['Bhuti'], ['Nitu'], ['Meenu'], ['Phunam'], ['Sunita'], ['Danisha'],
    ['Lakshmi'], ['Manju'], ['Komal'], ['Baby'], ['Puja'], ['Saroj'], ['Jammu'], ['Humari'], ['Roshan'], ['Vekha'],
    ['Krishna'], ['Priyanka'], ['Rashmi'], ['Ashi'], ['Munta'], ['Kamal'], ['Vabita'], ['Himlata'], ['Patashi'],
    ['Sima'], ['Sima'], ['Anita'], ['Manju'], ['Sapna'], ['Riya'], ['Shivi'], ['Rinku'], ['Kiran'], ['Saroj'], ['Padima'],
    ['Suman'], ['Madhuri'], ['Shivi'], ['Kavita'], ['Puja'], ['Manta'], ['Minto'], ['Mishri'], ['Anju'], ['Santra'],
    ['Mandini'], ['Manta'], ['Gita'], ['Manisha'], ['Deepa'], ['Semika'], ['Pushpa'], ['Nalini'], ['Hansa'], ['Rimla'],
    ['Sima'], ['Gita'], ['Priyanka'], ['Devi'], ['Priya'], ['Anita'], ['Riya'], ['Shambh'], ['Vandana'], ['Savitri']
]




    sheet.update(f"C1857:C1957",data)

   
if __name__ == "__main__":
    main()
