# this is a test version of the runner code

import notifier
import time

# store login info
login_credentials = notifier.getLoginInfo()

# notifier.notifyITTeam(function_origin="420", problem_description="test report", credentials=login_credentials)

def testFunctions():

    return None


def main():

    # pull all tickets that are not Solved
    ticket_list = notifier.getAllNotSolvedTickets(credentials=login_credentials, printResponse=True)

    # put together the email list
    response_list = notifier.compileEmailList(ticket_list=ticket_list)
    print('email_list contains', response_list)

    time.sleep(5)

    for i in range(0, len(response_list)):
        print('respond to:', response_list[i][0], 'ticket:', response_list[i][1])  # debugging
        notifier.makeTicket(emailAddress=response_list[i][0], credentials=login_credentials)
        
        # check response from makeTicket()
        # if the response from making the ticket < 200, the ticket was made successfully add automated response tag
        # if notifier.makeTicket(emailAddress=response_list[i], credentials=login_credentials)[0].status_code < 300:
        #     print('new ticket successfuly made for', response_list[0])
        # otherwise, add failed response tag and notify IT team
        # else:
        #     print('add response failed tag')
            # add failed response tag
            # notify IT team



testFunctions()
main()