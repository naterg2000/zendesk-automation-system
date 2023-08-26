# for more information about the Ticket API,
# visit https://developer.zendesk.com/api-reference/ticketing/tickets/tickets/

import requests
import re
import json
import time

# zendesk FYI subdomain
subdomain = "https://fyihelp.zendesk.com"

# use this phrase to look for the tag indicated a response email has already been sent
dont_resond_tag = "sent_automated_response"

# use this phrase to indicate a request ticket that was not able to be automatically responded to
response_failed_tag = "response_failed"

# don't email these users
email_blacklist = ['sunil@fyi.fyi']

# list of IT account emails
it_team_emails = ['nadia.underwood@fyi.fyi', 'fyiintern001@gmail.com']


# read login info from a file for extra security
# RETURN credentials: a list containing [0] = email, [1] = password
def getLoginInfo():

    try:
    # open login info file
        zd_login = open('login_info.txt', 'r')
    except:
        
        # email support team to address the login credentials issue
        notifyITTeam(function_origin="getLoginInfo()", problem_description="There was an issue reading the login info file", credentials=["fyiintern001@gmail.com", "Chocolate2020"])

        # stop the program since nothing will work if login info is different
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


# notify the IT team that something has gone wrong
# PARAM function_origin: the function where the notification is called; hardcoded value
# PARAM problem_description: a description to include in the ticket body about what's going on
# PARAM credentials: a list of the zendesk login info
# RETURN none: return nothing
def notifyITTeam(function_origin=None, problem_description=None, credentials=list):

    ticket_data = {
        "ticket": {

                # this is what the body of the ticket will be
                "comment": {    
                    "body": "There was an issue with the handler\n"
                    + "Function origin: " + function_origin + "\n"
                    + "Problem description: " + problem_description
                },

                # priority of the ticket is urgent since 
                # we want to get users back up and running quickly
                "priority": "urgent",

                # test notif, change this to something relevant to the reset request
                # set this to Don't Notify so Nadia and Intern account don't get an email
                # standard subject should be "Encryption Key Reset Follow-up"
                "subject": "Problem with Zendesk Handler System",
                # add a flag to the ticket tags so when we pull all 
                # ticket data we don't send another email to this user
                "tags": ["automated_message"]   
            }
    }


    # convert ticket data dict to JSON payload
    payload = json.loads(json.dumps(ticket_data))

    # set header(s) for HTTP request
    headers = {
        "Content-Type": "application/json",
    }

    # make the POST request
    response = requests.request(
        "POST",
        url=subdomain + "/api/v2/tickets/",
        auth=(credentials[0], credentials[1]),
        headers=headers,
        json=payload
    )

    printHTTPResponse(response, "POST")

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



# submit a POST request to make a new ticket
# PARAM endpoint: the API endpoint 
# PARAM new_ticket_info: a dictionary containg new ticket information to convert to JSON payload
# PARAM credentials: a list of login info for the API authenticatoin
# PARAM printResponse: print the HTTP response code, False by default will not print the code
# RETURN response: returns the HTTP response object
def submitPOST(endpoint="", new_ticket_info=dict, credentials=list, printResponse=False):

    if new_ticket_info == {}:
        print("empty dictionary passed to submitPOST()")
        return None

    # the content to send in the POST request
    payload = json.loads(json.dumps(new_ticket_info))
    # set header(s) for HTTP request
    headers = {
        "Content-Type": "application/json",
    }
    # make post request with payload
    # if the code is an error, try again 3 times
    # if after the third time it doesn't work, make a ticket for the IT team to respond to 
    post_attempts = 0
    while post_attempts < 3:

        # make the POST request
        response = requests.request(
            "POST",
            endpoint,
            auth=(credentials[0], credentials[1]),
            headers=headers,
            json=payload
        )

        # incremement post_attempts counter
        post_attempts = post_attempts + 1

        # wait 1 second to prevent overloading the API
        time.sleep(1)

        # if 3 attempts have been reached
        # if post_attempts == 2:
            # notifyITTeam(function_origin="submitPOST()", problem_description="could not POST ticket:\n", credentials=credentials)

            # put a flag to ignore the ticket in question
            # return None
        
        # if the code is less than 300, meaning it was not successful, try again
        # if 3 tries are exceeded
        if response.status_code < 300:
            break

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
        endpoint = subdomain + "/api/v2/tickets/" + str(ticket_id)  # api command to get the ticket's ID
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

    # if the code is an error, try again 3 times
    # if after the third time it doesn't work, make a ticket for the IT team to respond to 
    put_attempts = 0
    while put_attempts < 3:

        # make post request with payload
        response = requests.request(
            "PUT",
            endpoint,
            auth=(credentials[0], credentials[1]),
            headers=headers,
            json=payload
        )

        # incremement post_attempts counter
        put_attempts = put_attempts + 1

        # wait 1 second to prevent overloading the API
        time.sleep(1)

        # if 3 attempts have been reached
        if put_attempts == 2:
            print('Notify IT team to check what\'s up with this email and submit a manual ticket')
            notifyITTeam(function_origin="addResponseFailedTag()", 
                         problem_description="Could not upload automated_response_flag to ticket " + ticket_id, 
                        credentials=credentials)
            
            # add the response failed tag to the ticket
            addResponseFailedFlag(ticket_id=ticket_id, credentials=credentials)

        # if the code is less than 300, meaning it was not successful, try again
        # if 3 tries are exceeded
        if response.status_code < 300:
            break

    # if printResponse is True, print 
    if printResponse:
        printHTTPResponse(response, "PUT")
    return response




# add the response failed tag to the specified ticket with PUT. prewvent further attempts to reach out to this email
# PARAM ticket_id: a string with the ticket to add the flag to
# PARAM credentials: a list containig the [0] login email and [1] the login password
# PARAM printResponse: a bool; True will print the repsonse code of the request, False will bypass it
# RETURN response: returns the response code from the PUT request
def addResponseFailedFlag(ticket_id='', credentials=list, printResponse=False):

    endpoint = ""

    # check that a ticket ID was passed
    if ticket_id != "":
        endpoint = subdomain + "/api/v2/tickets/" + str(ticket_id)
    else:
        print("please enter ticket ID to add automated response flag to")
        return None
    
    # a dict of the content to add to the ticket
    update_tag_payload = {"ticket": {"tags": response_failed_tag}}

    # the content to send in the POST request
    payload = json.loads(json.dumps(update_tag_payload))
    # set header(s) for HTTP request
    headers = {
        "Content-Type": "application/json",
    }

    # if the code is an error, try again 3 times
    # if after the third time it doesn't work, make a ticket for the IT team to respond to 
    put_attempts = 0
    while put_attempts < 3:

        # make post request with payload
        response = requests.request(
            "PUT",
            endpoint,
            auth=(credentials[0], credentials[1]),
            headers=headers,
            json=payload
        )

        # incremement post_attempts counter
        put_attempts = put_attempts + 1

        # wait 1 second to prevent overloading the API
        time.sleep(1)

        # if 3 attempts have been reached
        if put_attempts == 2:
            print('Notify IT team to check what\'s up with this email and submit a manual ticket')
            notifyITTeam(function_origin="addResponseFailedTag()", 
                         problem_description="Could not upload response_failed_tag to ticket " + ticket_id, 
                        credentials=credentials)
            
        # if the code is less than 300, meaning it was not successful, try again
        # if 3 tries are exceeded
        if response.status_code < 300:
            break

    # if printResponse is True, print 
    if printResponse:
        printHTTPResponse(response, "PUT")
    return response






# makes a new zendesk ticket as a response to the encryption key reset requester. this will also send an email to the requester
# PARAM emailAddress: string of the email address for the new ticket
# PARAM ticket_info: a list containing [0]: the email address to respond to and [1]: the ticket's ID for merging
# PARAM credentials: a list containing the zendesk login info 
# RETURN new_ticket_result: list of [HTTPResponseObject, newTicketID], None if conditions were not satisfied
def makeTicket(emailAddress="", credentials=list):

    # make a list with 2 elements
    new_ticket_result = ['','']

    if emailAddress == "sunil@fyi.fyi":
        print("sunil's email, don't reply for now")
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

                # set this to Don't Notify so Nadia and Intern account don't get an email
                # standard subject should be "Encryption Key Reset Follow-up"
                "subject": "Don't Notify",  
                "requester": emailAddress,  
                "recipient": emailAddress,
            }
        }

        # print('sending an email to ', ticket_info[0]) # debugging

        # post new ticket to zendesk
        postAttempt = submitPOST(endpoint=endpoint, new_ticket_info=ticket_info, credentials=credentials, printResponse=True)
        
        
        if postAttempt == None:
            # add response failed tag
            print('adding response failed tag')
        else:
            # store HTTP result in [0]
            new_ticket_result[0] = postAttempt

            # if new ticket was successfully made, get status:new tickets
            new_tickets_response = submitGET(endpoint=subdomain + '/api/v2/search.json?query=type:ticket+status:new', credentials=credentials, printResponse=False)
            
            # store the http response as a json
            new_tickets_json = new_tickets_response.json()
            
            # break json up into a list
            new_ticket_list = new_tickets_json[list(new_tickets_json.keys())[0]]
            # find the new ticket with requester == emailAddress
            for new_ticket in new_ticket_list:
                # if the curent new ticket has the correct email address, store the ticket ID
                if new_ticket['recipient'] == emailAddress:

                    print('new ticket ID: ', new_ticket['id'])

                    # store the correct ID in new_ticket_result[1]
                    new_ticket_result[1] = new_ticket['id']
                    
            print('new_ticket_result:', new_ticket_result)
            return new_ticket_result

    else:
        if emailAddress == "":
            print('email address is empty in makeTicket')
        elif len(credentials) != 2:
            print('check credentials passed to makeTicket()')
        return None





# takes in a ticket data list and extracts the sender email with a regular expression
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
    




# marge specified ticket info into passed ticket ID
# PARAMS merge_ticket: ticket ID to grab comment from
# PARAMS target_ticket: ticket ID to add the merge_ticket comment from
# RETURN response: HTTP response from merging the tickets
def mergeTicketIntoTarget(merge_ticket='', target_ticket='', credentials=list):

    # print('merging ticket', merge_ticket, 'into', target_ticket)    # deubgging
    endpoint = subdomain + '/api/v2/tickets/' + target_ticket + '/merge'

    # grab ticket info from a ticket you'd like to add to another ticket
    merge_ticket_info_response = submitGET(endpoint=subdomain + '/api/v2/tickets/' + merge_ticket, credentials=credentials)
    merge_ticket_info_json = merge_ticket_info_response.json()

    # break up JSON response into a list
    merge_ticket_info = merge_ticket_info_json[list(merge_ticket_info_json.keys())[0]]

    # check that the merge info response was correct
    if merge_ticket_info_response.status_code > 299:
        print('merge ticket responded with', merge_ticket_info_response.status_code)    # debugging
    else:
        print('grabbed ticket', merge_ticket_info['id'])    # debugging

    # dictionary version of ticket body to merge into target_ticket
    merge_body = {
        "ids": [ merge_ticket ],
        "target_comment": "Request info from Ticket " + str(merge_ticket_info['id']) + "\n\n" + merge_ticket_info['description'],
    }

    # store the merge response
    merge_response = submitPOST(endpoint=endpoint, new_ticket_info=merge_body, credentials=credentials, printResponse=True)

    # check that the response from the merge was witihin the 200 range
    if merge_response.status_code > 299 or merge_response == None:
        print('Something went wrong with the merge')
    else:
        print('Merging ticket', merge_ticket_info['id'], 'was successful')

    return merge_response



# pull all tickets that are NOT solved
# PARAM credentials: list of login info for zendesk account
# RETURN ticket_data: list of tickets that are not solved
def getAllNotSolvedTickets(credentials=list, printResponse=False):
    # endpoint = subdomain + '/api/v2/search.json?query=type:ticket+status:pending+status:new+status:open'   # solved is the "largest" value of status, so anything less than solved is not-solved
    endpoint = subdomain + '/api/v2/search.json?query=type:ticket+status:open+status:pending+status:new' 
    
    # submit GET request for all not solved tickets
    response = submitGET(endpoint=endpoint, credentials=getLoginInfo(), printResponse=printResponse)

    # store the response as a JSON object
    data = response.json()

    # break up the JSON into a list
    ticket_data = data[list(data.keys())[0]]

    # return the list of broken up JSON data
    return ticket_data



# put together a list of address to make new tickets for emails we need to respond to come from help@fyi.fyi forwarded emails 
# with subject "Request reset encryption key". The ticket must also not have the tag "sentautomateresponse"
# PARAM ticket_list: a list of ticket data 
# RETURN response_list: a list of emails and ticket IDs from tickets that have the correct subject and do not have the don't send flag
def compileEmailList(ticket_list):

    # search for this subject when adding tickets to the email list
    search_subject = "Request reset encryption key"

    # look for this flag to avoid sending multiple responses to the same user
    dont_respond_flag = "sentautomatedresponse"

    # the list of emails to return
    response_list = list()

    # if there were no emails passed, just return an empty list
    if len(ticket_list) == 0:
        return response_list

    # look through each ticket in the list of tickets passed
    for ticket in ticket_list:
        
        # check for the correct subject for each ticket from the pulled list
        if ticket['subject'] == search_subject:
            
            # flag to determine whether to add the current email to the response list
            addEmailToList = True

            # look through the tags of the current ticket. If the don't respond tag is in
            # the tags of this ticket, set the add flag to false
            for tag in ticket['tags']:
                if dont_respond_flag in tag or response_failed_tag in tag:
                    addEmailToList = False
            
            # if the add flag remained true, add this email to the response list
            if addEmailToList:
                # extract the email from this ticket's descriptoin and add it to the response list
                response_list.append([extractSenderEmail(ticket_description=ticket['description']), ticket['id']])

    return response_list
