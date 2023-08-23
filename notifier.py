# for more information about the Ticket API,
# visit https://developer.zendesk.com/api-reference/ticketing/tickets/tickets/

import requests
import re
import json

subdomain = "https://fyihelp.zendesk.com"


# use this function to test functions
def runFunctions():

    ticket_to_make = {
        "ticket": {

            # this is what the body of the ticket will be
            "comment": {    
                "body": "This is a test ticket for sending a response to a benzo log"
            },

            # priority of the ticket is urgent since 
            # we want to get users back up and running quickly
            "priority": "urgent",

            # test notif, change this to something relevant to the reset request
            "subject": "Don't Notify",  
            "requester": "naterg2000@gmail.com",  

            # add a flag to the ticket tags so when we pull all 
            # ticket data we don't send another email to this user
            "tags": ["sentautomatedreseponse"]  
        }
    }
    # test GET method
    # submitGET(endpoint=subdomain+'/api/v2/tickets/recent', credentials=getLoginInfo(), printResponse=True)
    # submitPOST(endpoint=subdomain + "/api/v2/tickets", new_ticket_info=ticket_to_make, credentials=getLoginInfo(), printResponse=True)
    makeTicket(emailAddress="naterg2000@gmail.com", credentials=getLoginInfo())

    return None


# read login info from a file for extra security
def getLoginInfo():
    # open login info file
    zd_login = open('login_info.txt', 'r')
    # read a line from the file
    credentials = zd_login.readline()
    # split with commas and return the separated list
    return credentials.split(',')


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
        print('Response: ', response.status_code)
        if response.status_code >= 200 and response.status_code < 300:
            print("GET posted with no problem")
        elif response.status_code >= 300 and response.status_code < 400:
            print("GET has multiple response choices, check logic")
        elif response.status_code >= 400 and response.status_code < 500:
            print("Error with GET request, check syntax")
        elif response.status_code >= 500 and response.status_code < 600:
            print("There was an unexpected error with the server")
    return response


# submit the GET request to the specified endpoint
# PARAM endpoint: the API endpoint 
# PARAM credentials: a list of login credentials
# PARAM printResponse: print the code of the HTTP Response
# RETURN response: returns the HTTP response object
def submitGET(endpoint="", credentials=list, printResponse=False):
    # make api call
    response = requests.get(endpoint, auth=("fyiintern001@gmail.com", "Chocolate2020"))
    # if printResponse is True, print 
    if printResponse:
        print('Response: ', response.status_code)
        if response.status_code >= 200 and response.status_code < 300:
            print("GET posted with no problem")
        elif response.status_code >= 300 and response.status_code < 400:
            print("GET has multiple response choices, check logic")
        elif response.status_code >= 400 and response.status_code < 500:
            print("Error with GET request, check syntax")
        elif response.status_code >= 500 and response.status_code < 600:
            print("There was an unexpected error with the server")
    return response

# makes a new zendesk ticket as a response to the encryption key reset requester. this will also send an email to the requester
# PARAM emailAddress: string of the email address for the new ticket
# PARAM credentials: a list containing the zendesk login info 
# RETURN response: returns the HTTP response when attempting to make a new ticket, None if conditions were not satisfied
def makeTicket(emailAddress="", credentials=list):

    endpoint = subdomain + "/api/v2/tickets"

    # first, check if there was an email address passed and
    # credentials length is 2
    if emailAddress != "" and len(credentials) == 2:
        # continue with making the ticket
        print('continuing with making ticket')

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
                "subject": "Don't Notify",  
                "requester": emailAddress,  

                # add a flag to the ticket tags so when we pull all 
                # ticket data we don't send another email to this user
                "tags": ["sentautomatedreseponse"]  
            }
        }

        return submitPOST(endpoint=endpoint, new_ticket_info=ticket_info, credentials=credentials, printResponse=True)

    else:
        if emailAddress == "":
            print('email address is empty in makeTicket')
        elif len(credentials) != 2:
            print('check credentials passed to makeTicket()')
        return None


# takes in a ticket data list and extracts the sender email
# with regex. 
# return a string
def extractSenderEmail(ticket_description):

    # regular expression to search for "Email: <email>"
    email_expression = "Email: [A-Za-z0-9@._\-!#$%&'*+=?^_`{|}~]+.[a-z]+"

    # search the ticket description for the expression
    # split it by ":", [0] to select the only elment in the list
    emailInfo = re.findall(email_expression, ticket_description)[0].split(':')

    # remove spaces/whitespace
    emailInfo[1].strip()
    
    # tf there are only 2 elements in the list, they will be ['Email', <email>]
    # if anything went wrong, there will be more/less than 2 elements in the list
    if len(emailInfo) == 2:
        return emailInfo[1]
    else:
        return ""
    


# return ticket ID if the new tag is added
# return None if the newTag exists in the ticket's tags
def updateTicketTag(ticket=[], newTag=""):

    # if the new tag is not in the current tag
    for tag in ticket['tags']:
        if tag in newTag:
            return None 

    ticket['tags'].append(newTag)
    return ticket['id']



def getZendeskTickets():

    emailsToRespondTo = list()

    # get recent tickets
    endpoint = "https://fyihelp.zendesk.com/api/v2/tickets/recent"
    # endpoint = "https://fyihelp.zendesk.com/api/v2/tickets/379"
    user="fyiintern001@gmail.com"
    pwd="Chocolate2020"

    # make api call
    response = requests.get(endpoint, auth=(user, pwd))

    # if anything other than 200 is receieved, exit
    if response.status_code != 200:
      print('Status:', response.status_code, 'Problem with the request. Exiting.')
      # exit()

    # store response as json
    data = response.json()

    # break up the json response into lists of data
    ticket_data = data[list(data.keys())[0]] 

    # look through each ticket subject for "Request reset encryption key"
    search_for_subject = "Request reset encryption key"

    # if there was only 1 recent ticket, handle it separately
    if len(data) == 1:

        foundSentAutomatedResponse = False
        
        # look for sentautomatedresponse
        for i in ticket_data['tags']:
            if 'sentautomatedresponse' in i:
                foundSentAutomatedResponse = True

        # if sentautomatedresponse is not found, add this email to emailsToRespondTo
        if  not foundSentAutomatedResponse:
            emailsToRespondTo.append(extractSenderEmail(ticket_data['description']))

    # otherwise handle all recent tickets
    else:
        for i in range(0, len(ticket_data)):

            # store each ticket temporarily
            current_ticket = ticket_data[i]  

            extractSenderEmail(current_ticket['description'])
            
            # if the ticket subject is subject_for_search
            if search_for_subject in current_ticket['subject']:
                tags = current_ticket['tags']
                if len(tags) == 0:
                    # send reset request response
                    # since there are no labels, we know the automated repsonse
                    # was not sent
                    # makeTicket(emailAddress=extractSenderEmail(ticket_description=current_ticket['description']))
                    pass
                else:
                    # look through the ticket's tags to find
                    # sentautomatedresponse
                    for tag in current_ticket['tags']:
                        if "sentautomatedresponse" in tag:
                            # print('Can skip ticket', current_ticket['id'])
                            print()
                        else:
                            # print('send email response to', current_ticket['id'])
                            print()
        
    return emailsToRespondTo

runFunctions()