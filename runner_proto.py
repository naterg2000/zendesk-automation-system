# this is a test version of the runner code

# currently adding UI to this 

import notifier
import time
import os
from sys import platform


class ZendeskAutomationSystem():  

    login_credentials = notifier.getLoginInfo() # store login info
    update_frequency = 20    # the time between each API request
    system_status = "Hello there" 

    def changeUpdateFrequency(new_frequency=int):
        ZendeskAutomationSystem.update_frequency = new_frequency
        print(ZendeskAutomationSystem.update_frequency)
        return new_frequency 

    def handleResetRequests():

        try:
            print('grabbing non-solved tickets')    # logging
            ticket_list = notifier.getAllNotSolvedTickets(credentials=ZendeskAutomationSystem.login_credentials, printResponse=False)   # pull all tickets that are not Solved
            response_list = notifier.compileEmailList(ticket_list=ticket_list)  # put together the email list
            print('email_list contains', response_list) # logging
            time.sleep(ZendeskAutomationSystem.update_frequency)   # wait some time 

            for i in range(0, len(response_list)):
                make_ticket_response = notifier.makeTicket(emailAddress=response_list[i][0],
                                                        redentials=ZendeskAutomationSystem.login_credentials)
                print('attempting to respond to ', response_list[i][0])
                if make_ticket_response == None:
                    print('could not make response ticket -- add response failed tag')
                    notifier.addResponseFailedFlag(ticket_id=response_list[i][1], 
                                                credentials=ZendeskAutomationSystem.login_credentials, printResponse=True)

                    print('Notify IT team')
                    # notifier.notifyITTeam(params here)
                else:
                    print('successfully responded to', response_list[i][0])

                    # add response_successful tag to the original request ticket
                    notifier.addAutomatedResponseFlag(ticket_id=response_list[i][1], 
                                                    credentials=ZendeskAutomationSystem.login_credentials, printResponse=True)

                    # merge original request ticket into new ticket
                    notifier.mergeTicketIntoTarget(response_list[i][1], target_ticket_id=make_ticket_response[1], 
                                                credentials=ZendeskAutomationSystem.login_credentials)
        except KeyboardInterrupt:
            print("System stopped by user - Ctrl + C")
            exit()

    def main():

        while True: # continually run

            # clear the command line with every loop execution
            if platform == "win32":
                os.system('cls')
            else:
                os.system('clear')

            ZendeskAutomationSystem.handleResetRequests()

            


# ZendeskAutomationSystem.main()