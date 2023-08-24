# for more information about the Ticket API,
# visit https://developer.zendesk.com/api-reference/ticketing/tickets/tickets/

import requests
import re
import json

subdomain = "https://fyihelp.zendesk.com"

# use this phrase to look for the tag indicated a response email has already been sent
dont_resond_tag = "sentautomatedresponse"

# don't email these users
email_blacklist = ['sunil@fyi.fyi']


# read login info from a file for extra security
# RETURN credentials: a list containing [0] = email, [1] = password
def getLoginInfo():

    try:
    # open login info file
        zd_login = open('login_info.txt', 'r')
    except:
        print('Something went wrong trying to read login credentials')
        exit()
    else:
        # read a line from the file
        credentials = zd_login.readline()
        # split with commas and return the separated list
        return credentials.split(',')

# print an HTTP response code and what it means
# PARAM response: the HTTP response
# RETURN response: returns the HTTP response object
def printHTTPResponse(response, command):
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

# submit a POST request to make a new ticket
# PARAM endpoint: the API endpoint 
# PARAM new_ticket_info: a dictionary containg new ticket information to convert to JSON payload
# PARAM credentials: a list of login info for the API authenticatoin
# PARAM printResponse: print the HTTP response code, False by default will not print the code
# RETURN response: returns the HTTP response object
def submitPOST(endpoint="", new_ticket_info=dict, credentials=list, printResponse=False):
    # the content to send in the POST request
    payload = json.loads(json.dumps(new_ticket_info))
    # set header(s) for HTTP request
    headers = {
        "Content-Type": "application/json",
    }
    # make post request with payload
    response = requests.request(
        "POST",
        endpoint,
        auth=(credentials[0], credentials[1]),
        headers=headers,
        json=payload
    )
    # if printResponse is True, print 
    if printResponse:
        printHTTPResponse(response, "POST")
    return response


# add the automated response tag to the specified ticket with PUT
# PARAM ticket_id: a string with the ticket to add the flag to
# PARAM credentials: a list containig the [0] login email and [1] the login password
# PARAM printResponse: a bool; True will print the repsonse code of the request, False will bypass it
# RETURN response: returns the response code from the PUT request
def addAutomatedResponseFlag(ticket_id='', credentials=list, printResponse=False):

    endpoint = ""

    # check that a ticket ID was passed
    if ticket_id != "":
        endpoint = subdomain + "/api/v2/tickets/" + str(ticket_id)
    else:
        print("please enter ticket ID to add automated response flag to")
        return None
    
    # a dict of the content to add to the ticket
    update_tag_payload = {"ticket": {"tags": dont_resond_tag}}

    # the content to send in the POST request
    payload = json.loads(json.dumps(update_tag_payload))
    # set header(s) for HTTP request
    headers = {
        "Content-Type": "application/json",
    }

    # make post request with payload
    response = requests.request(
        "PUT",
        endpoint,
        auth=(credentials[0], credentials[1]),
        headers=headers,
        json=payload
    )
    # if printResponse is True, print 
    if printResponse:
        printHTTPResponse(response, "PUT")
    return response


# submit the GET request to the specified endpoint
# PARAM endpoint: the API endpoint 
# PARAM credentials: a list of login credentials
# PARAM printResponse: print the code of the HTTP Response
# RETURN response: returns the HTTP response object
def submitGET(endpoint="", credentials=list, printResponse=False):
    # make api call
    response = requests.get(endpoint, auth=(credentials[0], credentials[1]))
    # if printResponse is True, print 
    if printResponse:
        printHTTPResponse(response, "GET")
    return response


# makes a new zendesk ticket as a response to the encryption key reset requester. this will also send an email to the requester
# PARAM emailAddress: string of the email address for the new ticket
# PARAM credentials: a list containing the zendesk login info 
# RETURN response: returns the HTTP response when attempting to make a new ticket, None if conditions were not satisfied
def makeTicket(emailAddress="", credentials=list):

    for email in email_blacklist:
        if email == emailAddress:
            return None

    endpoint = subdomain + "/api/v2/tickets"

    # first, check if there was an email address passed and
    # credentials length is 2
    if emailAddress != "" and len(credentials) == 2:
        # continue with making the ticket

        # set ticket info
        ticket_info = {
            "ticket": {

                # this is what the body of the ticket will be
                "comment": {    
                    "body": "Thank you for reaching out to FYI Support!\n\nWe have received your request to reset your Encryption Key QR code.\
                        We will follow up with you as soon as we can in this Email thread.\n\nThank you for your patience. We will get you back into FYI soon!"
                },

                # priority of the ticket is urgent since 
                # we want to get users back up and running quickly
                "priority": "urgent",

                # test notif, change this to something relevant to the reset request
                # set this to Don't Notify so Nadia and Intern account don't get an email
                # standard subject should be "Encryption Key Reset Follow-up"
                "subject": "Don't Notify",  
                "requester": emailAddress,  
                "recipient": emailAddress,
                # add a flag to the ticket tags so when we pull all 
                # ticket data we don't send another email to this user
                "tags": ["sentautomatedreseponse"]  
            }
        }

        print('sending an email to ', emailAddress)

        return submitPOST(endpoint=endpoint, new_ticket_info=ticket_info, credentials=credentials, printResponse=True)

    else:
        if emailAddress == "":
            print('email address is empty in makeTicket')
        elif len(credentials) != 2:
            print('check credentials passed to makeTicket()')
        return None


# takes in a ticket data list and extracts the sender email with regex
# with regex. 
# PARAM ticket_description: the body of the ticket
# RETURN requesterEmail: a string with the requester's email
def extractSenderEmail(ticket_description):

    # regular expression to search for "Email: <email>"
    email_expression = "Email: [A-Za-z0-9@._\-!#$%&'*+=?^_`{|}~]+.[a-z]+"

    # search the ticket description for the expression
    # remove whitespace between Email: and <requester email>
    emailInfo = re.findall(email_expression, ticket_description)[0].replace(' ', '')

    # remove spaces/whitespace
    emailInfo = emailInfo.split(':')

    # if the split happened correctly, there should be 2 elements in emailInfo: [0] = "Email", [1] = <requester email>
    if len(emailInfo) == 2:
        return emailInfo[1]
    else:
        print('Something went wrong with extracting requester email')
        return None
    




# gets recent Zendesk tickets
# RETURN 
def getZendeskTickets():

    emailsToRespondTo = list()
    credentials = getLoginInfo()

    # get recent tickets
    # endpoint = "https://fyihelp.zendesk.com/api/v2/tickets/recent"    # for recent tickets
    # endpoint = "https://fyihelp.zendesk.com/api/v2/tickets/379"   # for a specific ticket ID
    response = submitGET(endpoint="https://fyihelp.zendesk.com/api/v2/tickets/recent", credentials=credentials, printResponse=False)

    # store response as json
    data = response.json()

    # if there was nothing returned from Zendesk, return emtpy list
    if len(data) == 0:
        print('No recent tickets')
        return []
    
    # if there was more than one ticket
    else:
        # break up the json response into lists of data
        ticket_data = data[list(data.keys())[0]] 

        # subject phrase to search for
        search_for_subject = "Request reset encryption key"

        # handle 1 ticket 
        if len(data) == 1:
            # if len(data) is 1, ticket_data will be a list of the ticket's info
            print('Handling one ticket')

            if search_for_subject == ticket_data['subject']:

                    print('Handling ticket ID ', ticket_data[i]['id'])  # debugging
                    print('Subject: ', ticket_data['subject'])   # debugging

                    # if there are no tags in this ticket -> make ticket
                    # no tags = no dont_respond_tag
                    if len(ticket_data['tags']) == 0:

                        current_ticket_id = ticket_data['id']

                        # get email address of this ticket
                        current_email = extractSenderEmail(ticket_data['description'])

                        # make a ticket for this email
                        # makeTicket(emailAddress=current_email, credentials=credentials)
                        print('pretending to send a ticket to', current_email)
                        emailsToRespondTo.append(current_email)

                        # add response flag to the current ticket
                        addAutomatedResponseFlag(ticket_id=current_ticket_id, credentials=credentials, printResponse=True)


        # handle multiple tickets with a loop
        else:
            print('Handling multiple tickets')

            # if len(data) > 1, each index of ticket_data will hold a ticket's info as a sub-list
            # for each element in ticket_data
            for i in range(0, len(ticket_data)):

                current_ticket = ticket_data[i]

                # before sending an automated response, we need to first check if the ticket is under
                # the correct subject
                # if the search phrase is in the current ticket's subject, continue
                if search_for_subject == current_ticket['subject']:

                    print('Handling ticket ID ', ticket_data[i]['id'])  # debugging
                    print('Subject: ', current_ticket['subject'])   # debugging

                    # if there are no tags in this ticket -> make ticket
                    # no tags = no dont_respond_tag
                    if len(current_ticket['tags']) == 0:

                        current_ticket_id = current_ticket['id']

                        # get email address of this ticket
                        current_email = extractSenderEmail(current_ticket['description'])

                        # make a ticket for this email
                        # makeTicket(emailAddress=current_email, credentials=credentials)
                        print('pretending to send a ticket to', current_email)
                        emailsToRespondTo.append(current_email)

                        # add response flag to the current ticket
                        addAutomatedResponseFlag(ticket_id=current_ticket_id, credentials=credentials, printResponse=True)

                    else:
                        # if the ticket has the correct subject,
                        # next check for the sentautomatedresponse tag
                        for tag in current_ticket['tags']:

                            if dont_resond_tag == tag:
                                print('Skip this ticket')   # debugging
                            else:
                                print('respond to ticket ', current_ticket['id'])   # debugging

                                # add this email to the list to respond to
                                emailsToRespondTo.append(current_email)

                                # add the responpse flag so the this ticket does not get responded to more than once
                                addAutomatedResponseFlag(ticket_id=current_ticket_id, credentials=credentials, printResponse=True)
                    print()

    return emailsToRespondTo
# runFunctions()