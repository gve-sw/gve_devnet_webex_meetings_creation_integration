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

import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()


class Webex_API_Connector():

    def __init__(self, token, expires_at):
        '''
        Initialize a Webex Connector object
        '''
        
        self.user_token = token
        self.token_expires_at = expires_at
        self.base_url = "https://webexapis.com/v1/"
        self.user_headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' +  self.user_token
            }

    @staticmethod
    def is_token_valid(expires_at):
        '''
        Returns if the token is valid or expired
        '''
        return expires_at != None and time.time() < expires_at


    def create_meetings(self, title, start_date, end_date, speaker_email, host_email, start_without_speaker):
        '''
        Creates one or more meetings with the Webex Rest API.
        See also: https://developer.webex.com/docs/api/v1/meetings/create-a-meeting
        '''
        
        method = "POST"
        url = self.base_url +"/meetings"
        
        payload = {}
        invitee = {}
        payload['title'] = title
        payload['start'] = start_date
        payload['end'] = end_date
        payload['allowAnyUserToBeCoHost'] = False
        payload['enabledJoinBeforeHost'] = False
        payload['joinBeforeHostMinutes'] = 0
        payload['unlockedMeetingJoinSecurity'] = "allowJoinWithLobby" #Host "let's in" every guest manually. Set to "allowJoin" if guest should be able to join as soon as host in the meeting
        payload['publicMeeting'] = False
        invitee['email'] = speaker_email
        invitee['coHost'] = True
        payload['invitees'] = [invitee]
        payload['sendEmail'] = True
        payload['hostEmail'] = host_email
        payload['timezone'] = "Europe/Paris"
         
        if start_without_speaker:
            payload['allowAnyUserToBeCoHost'] = True
            payload['enabledJoinBeforeHost'] = True
            payload['joinBeforeHostMinutes'] = 15
            payload['unlockedMeetingJoinSecurity'] = "allowJoin"
     
        response = self.execute_rest_call(method, url, payload)

        return response


    def get_meeting_info(self):
        '''
        Get list of meetings.
        See also:
        https://developer.webex.com/docs/api/v1/meetings/list-meetings
        '''
        
        method = "GET"
        url = self.base_url +"/meetings"

        response = self.execute_rest_call(method, url)

        return response


    def get_own_details(self):
        '''
        Get own Webex person details
        See also: https://developer.webex.com/docs/api/v1/people/get-my-own-details
        '''
        
        method = "GET"
        url = self.base_url + "/people/me"
        
        response = self.execute_rest_call(method, url)
        
        return response


    def execute_rest_call(self, method, url, payload={}):
        '''
        Execute a Rest API call based on the given method, url and payload. Return response json.
        '''

        response = requests.request(method, url, headers=self.user_headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(response.json())
        else:
            return response.json()

