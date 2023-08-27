# this is a test version of the runner code

import notifier
import time

# store login info
login_credentials = notifier.getLoginInfo()

    

def testFunctions():
    # newTicketID = notifier.makeTicket(emailAddress="naterg2000@gmail.com", credentials=login_credentials)[1]

    return None


def main():

    while True:

        print('grabbing non-solved tickets')

        # pull all tickets that are not Solved
        ticket_list = notifier.getAllNotSolvedTickets(credentials=login_credentials, printResponse=False)

        # put together the email list
        response_list = notifier.compileEmailList(ticket_list=ticket_list)
        print('email_list contains', response_list)

        time.sleep(5)

        for i in range(0, len(response_list)):
            print('respond to:', response_list[i][0], 'ticket:', response_list[i][1])  # debugging
            make_ticket_response = notifier.makeTicket(emailAddress=response_list[i][0], credentials=login_credentials)

            print('make ticket response contians: ', make_ticket_response)
            
            if make_ticket_response == None:
                print('could not make ticket -- add response failed tag')
                notifier.addResponseFailedFlag(ticket_id=response_list[i][1], credentials=login_credentials, printResponse=True)

                print('Notify IT team')
                # notifier.notifyITTeam(params here)
            else:
                print('successfully responded to', response_list[i][0])

                print('adding response succesful flag')
                notifier.addAutomatedResponseFlag(ticket_id=response_list[i][1], credentials=login_credentials, printResponse=True)

                print('merging original request from ticket', response_list[i][1], 'into ticket', make_ticket_response[1])
                notifier.mergeTicketIntoTarget(response_list[i][1], target_ticket_id=make_ticket_response[1], credentials=login_credentials)



# testFunctions()

while True:
    main()