# this is a test version of the runner code

import notifier
import time

def main():

    # store login info
    login_credentials = notifier.getLoginInfo()

    # begin loop
    while True:

        #print('Checking for key reset requests')   #debugging

        # pull recent tickets
        email_list = notifier.getZendeskTickets(login_credentials)

        print('There are', len(email_list), 'emails to respond to')
        for email in email_list: 
            print(email)
            notifier.makeTicket(emailAddress=email, credentials=login_credentials)

        # wait to prevent overloading API
        print('\n\nWaiting 2 seconds\n\n')
        time.sleep(2)

        # check for Benzo Log updates
        # print("checking for new benzo logs")    # debugging

        # wait to prevent overloading API


main()