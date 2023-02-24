# GVE DevNet Webex Meetings Creation Integration 

This demo show how to integrate the scheduling functionality of Webex Meetings into an existing 3rd party tool. The data of the created meetings is stored in a local Excel file. 

## Contacts
* Ramona Renner

## Solution Components
* Webex

## Workflow

![workflow](/IMAGES/workflow.png)

## High Level Design

![High level design of PoV](/IMAGES/high_level_design.png)


## Prerequisites
* Webex Account (see also section: Related Sandbox Environment)

This sample code can be tested with any Webex account with Webex Meetings functionality. Still, non admin accounts come with some limitations. These accounts can only schedule meetings for themselves and not for others. Admin accounts allow the creation of meetings for other users of the organization.


## Related Sandbox Environment

The [Cisco Webex Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/cf7eca30-b4e8-44be-a529-e25a1c078ab3?diagramType=Topology) demo instance provides developers with a full-featured sandbox Webex site (including admin access) designed to allow you to explore Webex functionality and develop proof-of-concept apps using the various Webex user/admin APIs and SDKs.


## Installation/Configuration

### Register an OAuth Integration

**OAuth Integrations**: Integrations are how you request permission to invoke the Webex REST API on behalf of a Webex Teams user. To do this securely, the API supports the OAuth2 standard, which allows third-party integrations to get a temporary access token for authenticating API calls. 

To register an integration with Webex Teams:
1. Log in to **developer.webex.com**
2. Click on your avatar at the top of the page and then select **My Webex Apps**
3. Click **Create a New App**
4. Click **Create an Integration** to start the wizard
5. Fill in the following fields of the form:
   * **Will this integration use a mobile SDK?**: No
   * **Integration name**
   * **Icon**
   * **App Hub Description**
   * **Redirect URI(s)**: http://localhost:5000/callback
   * **Scopes**: Select spark:all, meeting:schedules_read, meeting:schedules_write, meeting:admin_schedule_read and meeting:admin_schedule_write
6. Click **Add Integration**
7. After successful registration, you'll be taken to a different screen containing your integration's newly created Client ID and Client Secret and more. Copy the secret, ID and OAuth Authorization URL and store it safely. Please note, that the Client Secret will only be shown once for security purposes

  > To read more about Webex Integrations & Authorization and to find information about the different scopes, you can find information [here](https://developer.webex.com/docs/integrations)

### Set up the Sample App

8. Make sure you have [Python 3.8.10](https://www.python.org/downloads/) and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed.

9. (Optional) Create and activate a virtual environment for the project ([Instructions](https://docs.python.org/3/tutorial/venv.html))   

10. Access the created virtual environment folder
    ```
    cd [add name of virtual environment here] 
    ```

11. Clone this GitHub repository into the local folder:  
    ```
    git clone [add GitHub link here]
    ```
    * For GitHub link: 
      In GitHub, click on the **Clone or download** button in the upper part of the page > click the **copy icon**  
      ![/IMAGES/giturl.png](/IMAGES/giturl.png)
  * Or simply download the repository as zip file using 'Download ZIP' button and extract it

12. Access the downloaded folder:  
    ```
    cd gve_devnet_webex_meetings_creation_integration
    ```

13. Install all dependencies:
    ```
    pip3 install -r requirements.txt
    ```

14. Fill in your variables in the .env file. Feel free to leave the variable without note as is (for testing purpose): 

  ```python
    CLIENT_ID=[Add client ID from step 7] 
    CLIENT_SECRET=[Add client secret from step 7] 

    REDIRECT_URI=http://localhost:5000/callback
    AUTHORIZATION_BASE_URL=[Add first part of the OAuth Authorization URL from step 7, e.g. https://webexapis.com/v1/authorize]
    AUTH_TOKEN_URL=[Add first part of the OAuth Authorization URL and replace the string "authorize" with "access_token" from step 7, e.g. https://webexapis.com/v1/access_token]
    SCOPE=["spark:all", "meeting:schedules_read", "meeting:schedules_write", "meeting:admin_schedule_read", "meeting:admin_schedule_write"]

    CSV_FILE_PATH=[Add the path of the local storage CSV file, e.g. meetings.xlsx or /Users/xxx/Desktop/meetings.xlsx]
    CSV_FILE_TAB=[Add name of tab in CSV file to populate, e.g. Meetings]

  ```
> Note: Mac OS hides the .env file in the finder by default. View the demo folder for example with your preferred IDE to make the file visible.

> Note: The name of and tab within the local CSV file can be changed. Still, it is required that the file provides a tab with the provided name and the defined columns, as shown in the meetings.xlsx of this repository. 


## Usage

15. Start the flask application:   

```python3 app.py```

Navigate to http://localhost:5000 and follow the application workflow.


# Screenshots

![/IMAGES/screenshot.png](/IMAGES/screenshot.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.