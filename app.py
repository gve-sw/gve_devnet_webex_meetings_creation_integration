''' Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
'''

# Import Section
from flask import Flask, render_template, request, redirect, session, url_for
from requests_oauthlib import OAuth2Session

from meetings_xlsx_connector import Meetings_XLSX_Connector
from webex_api_connector import Webex_API_Connector

from dotenv import load_dotenv
import os
import json

app = Flask(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app.secret_key = os.urandom(24)

load_dotenv()

@app.route('/')
def index():
    try:
        return render_template('login.html')
    except Exception as e: 
        print(e)  
        return render_template('login.html', error=True, errormessage=e, errorcode="")


@app.route("/redirect")
def login():
    '''Step 1: User Authorization.
    Redirect the user/resource owner to the OAuth provider (i.e. Webex Teams)
    using a URL with a few key OAuth parameters.
    '''

    teams = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = teams.authorization_url(AUTHORIZATION_BASE_URL)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state

    print("Step 1: User Authorization. Session state:", state)

    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.
@app.route("/callback", methods=["GET"])
def callback():
    '''
    Step 2: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    '''

    auth_code = OAuth2Session(CLIENT_ID, state=session['oauth_state'], redirect_uri=REDIRECT_URI)
    token = auth_code.fetch_token(AUTH_TOKEN_URL, client_secret=CLIENT_SECRET,
                                  authorization_response=request.url)

    '''
    At this point you can fetch protected resources but lets save
    the token and show how this is done from a persisted token
    '''

    session['oauth_token'] = token

    print("Step 2: Retrieving an access token.")
    
    return redirect(url_for('.started'))


@app.route("/started", methods=["GET"])
def started():
    
    teams_token = session['oauth_token']
    
    print("Step 3: Set token")

    session['token'] = teams_token['access_token']
    session['expires_at']  = teams_token['expires_at']

    return redirect(url_for('meeting'))


@app.route("/meeting", methods=["GET","POST"])
def meeting():
    '''
    Route to provide meeting information.
    '''

    meetings_xlsx_connector.reset_stored_meetings_data()

    if request.method == 'POST':
        
        try:

            token = session.get("token", None)
            expires_at = session.get("expires_at", None)

            if token == None or Webex_API_Connector.is_token_valid(expires_at) == False:
                return render_template('login.html')

            else:
                webex_api_connector = Webex_API_Connector(token, expires_at)

                title = request.form.get("title")
                start_date = request.form.get("start_date")
                end_date = request.form.get("end_date")
                speaker_email = request.form.get("speaker_email")
                meeting_count = int(request.form.get("meeting_count"))
                start_without_speaker = request.form.get("start_without_speaker")
                host_email = webex_api_connector.get_own_details()['emails'][0]

                for i in range(meeting_count):
                    numbered_title = f"{title} (Number {i})"
                    meeting = webex_api_connector.create_meetings(numbered_title, start_date, end_date, speaker_email, host_email, start_without_speaker)
                    meetings_xlsx_connector.store_meetings_data(meeting, speaker_email)

                meetings = meetings_xlsx_connector.meetings_data

                return render_template('store.html', meetings = meetings, created = True, updated=False)
            
        except Exception as e:
            return render_template('meeting.html', error=True, errormessage=e, errorcode="", created = False, updated=False)
    else:
        return render_template('meeting.html', meetings = [], created = False, updated=False)


@app.route("/update", methods=["GET", "POST"])
def update():
    '''
    Route to show information of created meetings and to trigger the update of the local xlsx file.
    '''
    try:
        
        meetings = meetings_xlsx_connector.meetings_data

        meetings_xlsx_connector.append_meetings_data_in_xlsx(meetings)

        return render_template('store.html', meetings = meetings, created = True, updated=True)
    
    except Exception as e:
        return render_template('store.html', error=True, errormessage=e, errorcode="", created = False, updated=False)
    

if __name__ == "__main__":

    CLIENT_ID = os.environ['CLIENT_ID'] 
    CLIENT_SECRET = os.environ['CLIENT_SECRET']
    REDIRECT_URI = os.environ['REDIRECT_URI']  
    AUTHORIZATION_BASE_URL = os.environ['AUTHORIZATION_BASE_URL']
    AUTH_TOKEN_URL = os.environ['AUTH_TOKEN_URL']
    SCOPE = json.loads(os.environ['SCOPE']) 

    XLSX_FILE_PATH = os.environ['XLSX_FILE_PATH']
    XLSX_FILE_TAB = os.environ['XLSX_FILE_TAB']

    meetings_xlsx_connector = Meetings_XLSX_Connector(XLSX_FILE_PATH, XLSX_FILE_TAB)
    
    app.run(port='5000', debug=True)

