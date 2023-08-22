import requests
import re


# send the request response email
# return email recipient
def sendResponseEmail(emailAddress=""):
    print("sending response email to", emailAddress)
    return emailAddress



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

    # get recent tickets
    endpoint = "https://fyihelp.zendesk.com/api/v2/tickets/recent"
    user="fyiintern001@gmail.com"
    pwd="Chocolate2020"

    # make api call
    response = requests.get(endpoint, auth=(user, pwd))

    # if anything other than 200 is receieved, exit
    if response.status_code != 200:
      print('Status:', response.status_code, 'Problem with the request. Exiting.')
      exit()

    # store response as json
    data = response.json()

    # break up the json response into lists of data
    ticket_data = data[list(data.keys())[0]] 

    # look through each ticket subject for "Request reset encryption key"
    email_re = "Email: [A-Za-z0-9@._\-!#$%&'*+=?^_`{|}~]+.[a-z]+"
    search_for_subject = "Request reset encryption key"
    
    for i in range(0, len(ticket_data)):
        current_ticket = ticket_data[i]  # store each ticket temporarily
        
        # if the ticket subject is subject_for_search
        if search_for_subject in current_ticket['subject']:
            tags = current_ticket['tags']
            if len(tags) == 0:
                # send reset request response
                # since there are no labels, we know the automated repsonse
                # was not sent
                sendResponseEmail(emailAddress="")
            else:
                # look through the ticket's tags to find
                # sentautomatedresponse
                for tag in current_ticket['tags']:
                    if "sentautomatedresponse" in tag:
                        print('Can skip ticket', current_ticket['id'])
                    else:
                        print('send email response to', current_ticket['id'])

        


    return None


def main():
    getZendeskTickets()

    return None

# run code
main()