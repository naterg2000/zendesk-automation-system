# by Nathan for FYI :D
# for more information about the Ticket API,
# visit https://developer.zendesk.com/api-reference/ticketing/tickets/tickets/
# documentation: https://docs.google.com/spreadsheets/d/1bICGrBglo_UzkocTmtVSYxzLoqfPwKsd-ZwSGDQl3Kg/edit?usp=sharing
# Zendesk API limit is 400 calls/minute - I think

import requests
import re
import json
import time

debug_mode = False  # NOT IMPLEMETNED YET -- debug flag to enable/disable printing, Don't Notify subject for new tickets, etc...
subdomain = "https://fyihelp.zendesk.com"   # zendesk FYI subdomain
search_subject = "Request reset encryption key" # search for this subject when adding tickets to the email list
dont_resond_tag = "response_successful" # use this phrase to look for the tag indicated a response email has already been sent
response_failed_tag = "response_failed" # use this phrase to indicate a request ticket that was not able to be automatically responded to
email_blacklist = ['']  # don't email these users -- add emails if needed
it_team_emails = ['nadia.underwood@fyi.fyi', 'fyiintern001@gmail.com']  # list of IT account emails


def getLoginInfo():
    """ Read login info from a .txt file 
    
    Returns: 
    credentials - a list containing [0] = email, [1] = password
    """

    try:    # open login info file
        zd_login = open('login_info.txt', 'r')
    except:
        # email support team to address the login credentials issue
        # notifyITTeam(function_origin="getLoginInfo()", 
        #               problem_description="There was an issue reading the login info file", 
        #               credentials=["fyiintern001@gmail.com", "Chocolate2020"])

        exit()  # stop the program since nothing will work if login info is different
    else:   
        credentials = zd_login.readline()   # read a line from the file
        zd_login.close() 
        return credentials.split(',')   # split with commas and return the separated list


def printHTTPResponse(response, command):
    """ Prints the command and HTTP response, returns the HTTP response

    Arguments:
    response: an HTTP response object
    command: the HTTP command like GET, POST, PUT

    Returns: 
    response - the HTTP response object that was passed
    """

    # print the response status code followed by the command and the possible reason
    # for the status code
    print('Response: ', response.status_code)
    if response.status_code >= 200 and response.status_code < 300:
        print(command, ": posted with no problem")

    elif response.status_code >= 300 and response.status_code < 400:
        print(command, ": has multiple response choices, check logic")

    elif response.status_code >= 400 and response.status_code < 500: 
        print(command, ": error with request, check syntax")

    elif response.status_code >= 500 and response.status_code < 600: 
        print(command, ": there was an unexpected error with the server")


    return response

"""

This is not used yet

"""
def notifyITTeam(function_origin=None, problem_description=None, credentials=list):
    """ Notifies the IT team that something did not work properly
    
    Arguments:
    function_origin: a String telling us where this function was called from
    problem_decsription: a String telling us giving us a hint of what went wrong
    credentials: a list containing [0] login email, [1] login password
    
    Returns: 
    no return value
    """

    ticket_data = {
        "ticket": {

                # this is what the body of the ticket will be
                "comment": {    
                    "body": "There was an issue with the handler\n"
                    + "Function origin: " + function_origin + "\n"
                    + "Problem description: " + problem_description
                },
                "priority": "urgent",   # priority of the ticket is urgent since we want to get users back up and running quickly

                # set this to "Don't Notify" so Nadia and Intern account don't get an email
                # standard subject should be "Encryption Key Reset Follow-up"
                "subject": "Problem with Zendesk Handler System",

                # add a flag to the ticket tags so when we pull all 
                # ticket data we don't send another email to this user
                "tags": ["automated_message"]   
            }
    }

    payload = json.loads(json.dumps(ticket_data))   # convert ticket data dict to JSON payload
    headers = { # set header(s) for HTTP request
        "Content-Type": "application/json",
    }

    try:
        response = requests.request(    # make the POST request
            "POST",
            url=subdomain + "/api/v2/tickets/",
            auth=(credentials[0], credentials[1]),
            headers=headers,
            json=payload
        )
    except Exception:
        print('Failed to submit POST')

    printHTTPResponse(response, "POST") # print the response of the POST request

    return response


def submitGET(endpoint="", credentials=list, printResponse=False):
    """ submit the GET request to the specified endpoint

    Arguments:
    endpoint: the API request endpoint
    credentials: a list containing [0] login email, [1] login password
    printResponse: a bool specifing whether to print the result of the HTTP response
    
    Returns: 
    response - the HTTP response from the GET request
    """
    try:
        response = requests.get(endpoint, auth=(credentials[0], credentials[1]))    # make API call

    except Exception:
        print('Failed to submit GET')
    

    if printResponse:   # if printResponse is True, print 
        printHTTPResponse(response, "GET")

    return response



def submitPOST(endpoint="", new_ticket_info=dict, credentials=list, printResponse=False):
    """ Submit the POST request to make a new ticket
    
    Arguments:
    endpoint: the API endpoint 
    new_ticket_info: a dictionary containg new ticket information to convert to JSON payload 
    credentials: a list of login info for the API authenticatoin
    printResponse: print the HTTP response code, False by default will not print the code
    
    Returns:
    response: returns the HTTP response object 
    """

    # if there was nothing passed for the new ticket information, return None
    if new_ticket_info == {}:
        print("empty dictionary passed to submitPOST()")
        return None

    payload = json.loads(json.dumps(new_ticket_info))   # the content to send in the POST request
    headers = { # set header(s) for HTTP request
        "Content-Type": "application/json",
    }

    # make post request with payload
    try:
        # make the POST request
        response = requests.request(
            "POST",
            endpoint,
            auth=(credentials[0], credentials[1]),
            headers=headers,
            json=payload
        )
    except Exception:
        print('Failed to submit POST -- submitPOST()')


    # if printResponse is True, print 
    if printResponse:
        printHTTPResponse(response, "POST")

    return response


def addAutomatedResponseFlag(ticket_id='', credentials=list, printResponse=False):
    """ Add the automated response tag to the specified ticket with PUT

    Arguments:
    ticket_id: a string with the ticket to add the flag to
    credentials: a list containig the [0] login email, [1] login password
    printResponse: a bool that will print the repsonse code of the request

    Returns:
    response: returns the response code from the PUT request
    """

    endpoint = ""   # API request endpoint

    # check that a ticket ID was passed for the endpoint
    if ticket_id != "":
        endpoint = subdomain + "/api/v2/tickets/" + str(ticket_id)  
    else:
        print("please enter ticket ID to add automated response flag to")
        return None
    
    update_tag_payload = {"ticket": {"tags": dont_resond_tag}}  # a dict of the content to add to the ticket
    payload = json.loads(json.dumps(update_tag_payload))    # the content to send in the POST request
    headers = { # set header(s) for HTTP request
        "Content-Type": "application/json",
    }

    try:
        # make post request with payload
        response = requests.request(
            "PUT",
            endpoint,
            auth=(credentials[0], credentials[1]),
            headers=headers,
            json=payload
        )
    except Exception:
        print('Failed to PUT -- addAutomatedResponseTag()')


    # if printResponse is True, print 
    if printResponse:
        printHTTPResponse(response, "PUT")

    return response


def addResponseFailedFlag(ticket_id='', credentials=list, printResponse=False):
    """ Add the response failed tag to the specified ticket with PUT. Prevent further attempts to reach out to this email

    Arguments:
    ticket_id: a string with the ticket to add the flag to
    credentials: a list containig the [0] login email, [1] the login password
    printResponse: a bool that will print the repsonse code of the request

    Returns:
    response: returns the response code from the PUT request
    """

    endpoint = ""   # the API request endpoint

    # check that a ticket ID was passed
    if ticket_id != "":
        endpoint = subdomain + "/api/v2/tickets/" + str(ticket_id)
    else:
        print("please enter ticket ID to add failed response flag to")
        return None
    
    
    update_tag_payload = {"ticket": {"tags": response_failed_tag}}  # a dict of the content to add to the ticket
    payload = json.loads(json.dumps(update_tag_payload))    # the content to send in the POST request
    headers = { # set header(s) for HTTP request
        "Content-Type": "application/json",
    }
  
    try:
        # make post request with payload
        response = requests.request(
            "PUT",
            endpoint,
            auth=(credentials[0], credentials[1]),
            headers=headers,
            json=payload
        )
    except Exception:
        print('Failed to submit PUT -- addResponseFailedTag()')


    # if printResponse is True, print 
    if printResponse:
        printHTTPResponse(response, "PUT")
        
    return response


def makeTicket(emailAddress="", credentials=list):
    """ Makes a new Zendesk ticket as a response to the Encryption Key Reset requester. They receive an email notification from Zendesk
    
    Arguments:
    emailAddress: string of the email address for the new ticket
    ticket_info: a list containing [0]: the email address to respond to and [1]: the ticket's ID for merging
    credentials: a list containing the Zendesk login info: [0] login email address, [1] login password

    Returns:
    new_ticket_result: list with [HTTPResponseObject, newTicketID], None if conditions were not satisfied
    """

    new_ticket_result = ['',''] # make the return list
    endpoint = subdomain + "/api/v2/tickets"    # set API endpoint

    # first, check if there was an email address passed and credentials length is 2
    if emailAddress != "" and len(credentials) == 2:

        # set ticket info
        ticket_info = {
            "ticket": {

                # this is what the body of the ticket will be
                "comment": {    
                    "body": "Thank you for reaching out to FYI Support!\n\nWe have received your request to reset your Encryption Key QR code.\
                        We will follow up with you as soon as we can in this Email thread.\n\nThank you for your patience. We will get you back into FYI soon!"
                },

                # priority of the ticket is urgent since we want to get users back up and running quickly
                "priority": "urgent",

                # set this to Don't Notify so Nadia and Intern account don't get an email
                # standard subject should be "Encryption Key Reset Follow-up"
                "subject": "Don't Notify" if debug_mode else "Encryption Key Reset Follow-up",  # add inline if: "Don't Notify" if debug_mode else "Encryption Key Reset Follow-up"
                "requester": emailAddress,  
                "recipient": emailAddress,
            }
        }

        post_attempt = submitPOST(endpoint=endpoint, new_ticket_info=ticket_info, credentials=credentials, printResponse=True)  # post new ticket to zendesk
        time.sleep(5)   # wait for Zendesk Ticket list to update  

        post_attempt_data = post_attempt.json() # store the new ticket attempt HTTP response as JSON
        new_ticket_data = post_attempt_data[list(post_attempt_data.keys())[0]]  # split the JSON into a list with ticket data
        new_ticket_result = [post_attempt, new_ticket_data['id']]   # store return list as [HTTP response from making the new ticket, new ticket ID]

        return new_ticket_result
    
    # if there was something wrong with the values passed, print it here and return none
    else:
        if emailAddress == "":
            print('email address is empty in makeTicket')
        elif len(credentials) != 2:
            print('check credentials passed to makeTicket()')

        return None


def extractSenderEmail(ticket_description):
    """ Takes in a ticket data list and extracts the sender email with a regular expression

    Arguments:
    ticket_description: the body of the ticket

    Returns:
    requesterEmail: a string with the requester's email
    """

    email_expression = "Email: [A-Za-z0-9@._\-!#$%&'*+=?^_`{|}~]+.[a-z]+"   # regular expression to search for "Email: <email>"

    # search the ticket description for the expression
    # remove whitespace between Email: and <email>
    emailInfo = re.findall(email_expression, ticket_description)[0].replace(' ', '')

    # remove spaces/whitespace
    emailInfo = emailInfo.split(':')    

    # if the split happened correctly, there should be 2 elements in emailInfo: [0] = "Email", [1] = <requester email>
    if len(emailInfo) == 2:
        return emailInfo[1]
    else:
        print('Something went wrong with extracting requester email')
        return None
    

def mergeTicketIntoTarget(original_request_ticket_id='', target_ticket_id='', credentials=list):
    """ Merge specified ticket info into passed ticket ID
    
    Arguments:
    original_request_ticket_id: ticket ID to grab comment from
    target_ticket_id: ticket ID to add the merge_ticket comment from

    Returns:
    response: HTTP response from merging the tickets
    """

    endpoint = subdomain + '/api/v2/tickets/' + str(target_ticket_id) + '/merge'

    # grab ticket info from a ticket you'd like to add to another ticket
    original_ticket_info_response = submitGET(endpoint=subdomain + '/api/v2/tickets/' + str(original_request_ticket_id), credentials=credentials)

    # check that the merge info response was correct
    if original_ticket_info_response.status_code > 299:
        print('mergeTicketIntoTarget(): grabbing old ticket info responded with:', original_ticket_info_response.status_code)    # debugging
        return None

    original_ticket_info_json = original_ticket_info_response.json()    # split response object into JSON
    original_ticket_info = original_ticket_info_json[list(original_ticket_info_json.keys())[0]] # break up JSON response into a list

    # dictionary version of ticket body to merge into target_ticket
    merge_body = {
        "ids": [ original_request_ticket_id ],
        "target_comment": "Request info from Ticket " + str(original_ticket_info['id']) + "\n\n" + original_ticket_info['description'],
    }
    
    merge_response = submitPOST(endpoint=endpoint, new_ticket_info=merge_body, credentials=credentials, printResponse=True) # execute ticket merge and store the merge response

    # check that the response from the merge was witihin the 200 range
    if merge_response.status_code > 299 or merge_response == None:
        print('Something went wrong with the merge')
    else:
        print('Merging ticket', original_ticket_info['id'], 'with', target_ticket_id, 'was successful')

    return merge_response


def getAllNotSolvedTickets(credentials=list, printResponse=False):
    """ Get all tickets that are not solved
    
    Arguments:
    credentials: list of login info for zendesk account

    Returns:
    ticket_data: list of tickets, and their data, that are not solved
    """

    # endpoint = subdomain + '/api/v2/search.json?query=type:ticket+status:pending+status:new+status:open'   # solved is the "largest" value of status, so anything less than solved is not-solved
    endpoint = subdomain + '/api/v2/search.json?query=type:ticket+status:new'    
    
    # submit GET request for all not solved tickets
    response = submitGET(endpoint=endpoint, credentials=credentials, printResponse=printResponse)
    data = {}
    try:
        data = response.json()  # store the response as a JSON object
    except Exception:
        return []
    ticket_data = data[list(data.keys())[0]]    # break up the JSON into a list

    return ticket_data


def compileEmailList(ticket_list):
    """ Put together a list of email address from Encryption Key Reset requests to make new tickets for

    Arguments:
    ticket_list: a list of ticket data 

    Returns:
    response_list: a list of emails and ticket IDs from tickets that have the correct subject and do not have any response flags
    """
    
    response_list = list()  # the list of emails to return

    # if there were no emails passed, just return an empty list
    if len(ticket_list) == 0:
        return response_list

    # look through each ticket in the list of tickets passed
    for ticket in ticket_list:
        
        if ticket['subject'] == search_subject: # check for the correct subject for each ticket from the pulled list
            addEmailToList = True   # flag to determine whether to add the current email to the response list

            for tag in ticket['tags']:  # look through the tags of the current ticket. If the don't respond tag is in
                if dont_resond_tag in tag or response_failed_tag in tag:    # the tags of this ticket, set the add flag to false
                    addEmailToList = False
            
            if addEmailToList:  # if the add flag remained true, add this email to the response list
                # extract the email from this ticket's descriptoin and add it to the response list
                response_list.append([extractSenderEmail(ticket_description=ticket['description']), ticket['id']])

    return response_list