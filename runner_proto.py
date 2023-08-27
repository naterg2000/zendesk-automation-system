# this is a test version of the runner code

import notifier
import time

# store login info
login_credentials = notifier.getLoginInfo()

# notifier.notifyITTeam(function_origin="420", problem_description="test report", credentials=login_credentials)

def testFunctions():

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
            
            make_ticket_response = 1 # debugging, delete me
            if make_ticket_response == None:
                print('could not make ticket -- add response failed tag')
                notifier.addResponseFailedFlag(ticket_id=response_list[i][1], credentials=login_credentials, printResponse=True)

                print('Notify IT team')
                # notifier.notifyITTeam(params here)
            else:
                print('successfully responded to', response_list[i][0])

                print('adding response succesful flag')
                notifier.addAutomatedResponseFlag(ticket_id=response_list[i][1], credentials=login_credentials, printResponse=True)



# testFunctions()

while True:
    main()