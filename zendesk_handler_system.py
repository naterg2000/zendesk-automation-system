import notifier
import system_ui
import time

# store login info
login_credentials = notifier.getLoginInfo()

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
            make_ticket_response = notifier.makeTicket(emailAddress=response_list[i][0], credentials=login_credentials)
            
            if make_ticket_response == None:
                print('could not make response ticket -- add response failed tag')
                notifier.addResponseFailedFlag(ticket_id=response_list[i][1], credentials=login_credentials, printResponse=True)

                print('Notify IT team')
                # notifier.notifyITTeam(params here)
            else:
                print('successfully responded to', response_list[i][0])

                # add response_successful tag to the original request ticket
                notifier.addAutomatedResponseFlag(ticket_id=response_list[i][1], credentials=login_credentials, printResponse=True)

                # merge original request ticket into new ticket
                notifier.mergeTicketIntoTarget(response_list[i][1], target_ticket_id=make_ticket_response[1], credentials=login_credentials)


# while True:
    # main()