# Copyright (c) 2023 Cisco and/or its affiliates.

# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at

#                https://developer.cisco.com/docs/licenses

# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.


from openpyxl import load_workbook

class Meetings_XLSX_Connector():
    
    def __init__(self, path, tab):
        '''
        Initialize Meetings XLSX connector
        '''
        
        self.path = path
        self.workbook = load_workbook(path)
        self.tab = tab
        self.meetings_data = []


    def store_meetings_data(self, meeting, speaker_email):
        '''
        Stores selected information of a meeting in the meetings_data list variable. 
        Expected input: speaker email address and meeting json returned from Webex Rest API after creating a meeting (see: https://developer.webex.com/docs/api/v1/meetings/create-a-meeting)
        '''
        
        meeting_excel_entry = [
            meeting['title'],
            meeting['meetingNumber'],
            meeting['id'],
            meeting['webLink'],
            meeting['start'],
            meeting['end'],
            meeting['hostEmail'],
            speaker_email
        ]

        self.meetings_data.append(meeting_excel_entry)


    def reset_stored_meetings_data(self):
        '''
        Resets the meetings_data list variable.
        '''
        self.meetings_data = []


    def append_meetings_data_in_xlsx(self, meetings):
        '''
        Adds the in advance gathered meetings' data (see store_meetings_data()) to the local meetings Excel file. 
        Excel file needs a Meetings tab. Columns should match the values defined in store_meetings_data().
        '''

        sheet = self.workbook[self.tab]
        
        for meeting in meetings:
            sheet.append(meeting)
        
        self.workbook.save(self.path)

