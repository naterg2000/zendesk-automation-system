import notifier
import time
import os
from sys import platform

login_credentials = notifier.getLoginInfo() # store login info
update_frequency = 120    # the time between each API request

def main():

    while True: # continually run
        try:
            print('running')
            print('grabbing non-solved tickets')    # logging
            ticket_list = notifier.getAllNotSolvedTickets(credentials=login_credentials, printResponse=False)   # pull all tickets that are not Solved
            response_list = notifier.compileEmailList(ticket_list=ticket_list)  # put together the email list
            # print('email_list contains', response_list) # logging

            # for each email in the response list
            for i in range(0, len(response_list)):
                make_ticket_response = notifier.makeTicket(emailAddress=response_list[i][0],
                                                        redentials=login_credentials)
                
                if make_ticket_response == None:
                    print('could not make response ticket -- add response failed tag')
                    notifier.addResponseFailedFlag(ticket_id=response_list[i][1], 
                                                credentials=login_credentials, printResponse=True)

                    print('Notify IT team')
                    # notifier.notifyITTeam(params here)
                else:
                    print('successfully responded to', response_list[i][0])

                    # add response_successful tag to the original request ticket
                    notifier.addAutomatedResponseFlag(ticket_id=response_list[i][1], 
                                                    credentials=login_credentials, printResponse=True)

                    # merge original request ticket into new ticket
                    notifier.mergeTicketIntoTarget(response_list[i][1], target_ticket_id=make_ticket_response[1], 
                                                credentials=login_credentials)
                    
            
            # clear the terminal
            if platform == "darwin":
                # OS X
                os.system('clear')
            if platform == "win32":
                # Windows
                os.system('cls')

            time.sleep(update_frequency)   # wait some time 

        except KeyboardInterrupt:
            print("System stopped by user - Ctrl + C")
            exit()
main()