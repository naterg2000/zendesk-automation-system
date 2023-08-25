# this is a test version of the runner code

import notifier
import time

# store login info
login_credentials = notifier.getLoginInfo()

def main():

    # pull all tickets that are not Solved
    ticket_list = notifier.getAllNotSolvedTickets(credentials=login_credentials, printResponse=True)

    # put together the email list
    email_list = notifier.compileEmailList(ticket_list=ticket_list)
    print('email_list contains', email_list)

    # make new tickets for each email in email_list
    # for email in email_list:
        # notifier.makeTicket(emailAddress=email, credentials=login_credentials)

main()